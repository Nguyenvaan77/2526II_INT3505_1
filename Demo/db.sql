-- =========================
-- 1. CREATE SCHEMA
-- =========================
CREATE SCHEMA IF NOT EXISTS medical_asset;
SET search_path TO medical_asset;

-- =========================
-- 2. ROLE & USER
-- =========================
CREATE TABLE role (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE department (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE app_user (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    department_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user_department
        FOREIGN KEY (department_id) REFERENCES department(id)
);

CREATE TABLE user_role (
    user_id BIGINT,
    role_id BIGINT,
    PRIMARY KEY (user_id, role_id),

    FOREIGN KEY (user_id) REFERENCES app_user(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES role(id) ON DELETE CASCADE
);

-- =========================
-- 3. ASSET DOMAIN
-- =========================
CREATE TABLE manufacturer (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE asset_type (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    maintenance_cycle_days INT CHECK (maintenance_cycle_days > 0)
);

CREATE TABLE asset (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    serial_number VARCHAR(100) UNIQUE,
    purchase_date DATE,
    purchase_price NUMERIC(15,2) CHECK (purchase_price >= 0),
    status VARCHAR(30) NOT NULL,
    department_id BIGINT,
    asset_type_id BIGINT,
    manufacturer_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (department_id) REFERENCES department(id),
    FOREIGN KEY (asset_type_id) REFERENCES asset_type(id),
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturer(id),

    CONSTRAINT chk_asset_status
        CHECK (status IN ('AVAILABLE', 'IN_USE', 'UNDER_MAINTENANCE', 'BROKEN', 'RETIRED'))
);

-- =========================
-- 4. MAINTENANCE
-- =========================
CREATE TABLE maintenance_schedule (
    id BIGSERIAL PRIMARY KEY,
    asset_id BIGINT NOT NULL,
    scheduled_date DATE NOT NULL,
    completed_date DATE,
    status VARCHAR(30) NOT NULL,
    note TEXT,

    FOREIGN KEY (asset_id) REFERENCES asset(id),

    CONSTRAINT chk_maintenance_status
        CHECK (status IN ('SCHEDULED', 'IN_PROGRESS', 'DONE', 'OVERDUE', 'CANCELLED'))
);

-- =========================
-- 5. SERVICE & REPAIR
-- =========================
CREATE TABLE service_request (
    id BIGSERIAL PRIMARY KEY,
    asset_id BIGINT NOT NULL,
    reported_by BIGINT NOT NULL,
    assigned_engineer_id BIGINT,
    description TEXT,
    priority VARCHAR(20),
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (asset_id) REFERENCES asset(id),
    FOREIGN KEY (reported_by) REFERENCES app_user(id),
    FOREIGN KEY (assigned_engineer_id) REFERENCES app_user(id),

    CONSTRAINT chk_sr_status
        CHECK (status IN ('PENDING', 'ASSIGNED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')),

    CONSTRAINT chk_sr_priority
        CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL'))
);

CREATE TABLE service_log (
    id BIGSERIAL PRIMARY KEY,
    service_request_id BIGINT NOT NULL,
    engineer_id BIGINT NOT NULL,
    problem_cause TEXT,
    resolution TEXT,
    repair_cost NUMERIC(12,2) DEFAULT 0 CHECK (repair_cost >= 0),
    started_at TIMESTAMP,
    finished_at TIMESTAMP,

    FOREIGN KEY (service_request_id) REFERENCES service_request(id) ON DELETE CASCADE,
    FOREIGN KEY (engineer_id) REFERENCES app_user(id)
);

-- =========================
-- 6. INVENTORY & PARTS
-- =========================
CREATE TABLE replacement_part (
    id BIGSERIAL PRIMARY KEY,
    part_code VARCHAR(100) UNIQUE,
    name VARCHAR(255) NOT NULL,
    unit_price NUMERIC(12,2) CHECK (unit_price >= 0)
);

CREATE TABLE inventory (
    id BIGSERIAL PRIMARY KEY,
    part_id BIGINT UNIQUE NOT NULL,
    quantity INT NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    min_threshold INT DEFAULT 5 CHECK (min_threshold >= 0),

    FOREIGN KEY (part_id) REFERENCES replacement_part(id)
);

CREATE TABLE used_part (
    id BIGSERIAL PRIMARY KEY,
    service_log_id BIGINT NOT NULL,
    part_id BIGINT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),

    FOREIGN KEY (service_log_id) REFERENCES service_log(id) ON DELETE CASCADE,
    FOREIGN KEY (part_id) REFERENCES replacement_part(id)
);

-- =========================
-- 7. CONTRACT
-- =========================
CREATE TABLE contract (
    id BIGSERIAL PRIMARY KEY,
    manufacturer_id BIGINT,
    asset_id BIGINT,
    start_date DATE,
    end_date DATE,
    details TEXT,

    FOREIGN KEY (manufacturer_id) REFERENCES manufacturer(id),
    FOREIGN KEY (asset_id) REFERENCES asset(id),

    CONSTRAINT chk_contract_date
        CHECK (end_date IS NULL OR end_date >= start_date)
);

-- =========================
-- 8. DEPRECIATION
-- =========================
CREATE TABLE depreciation_record (
    id BIGSERIAL PRIMARY KEY,
    asset_id BIGINT NOT NULL,
    method VARCHAR(30) NOT NULL,
    value NUMERIC(15,2) NOT NULL CHECK (value >= 0),
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (asset_id) REFERENCES asset(id),

    CONSTRAINT chk_dep_method
        CHECK (method IN ('STRAIGHT_LINE', 'DECLINING_BALANCE'))
);

-- =========================
-- 9. TRIGGER: AUTO DEDUCT INVENTORY
-- =========================
CREATE OR REPLACE FUNCTION deduct_inventory()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT quantity FROM inventory WHERE part_id = NEW.part_id) < NEW.quantity THEN
        RAISE EXCEPTION 'Insufficient stock';
    END IF;

    UPDATE inventory
    SET quantity = quantity - NEW.quantity
    WHERE part_id = NEW.part_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_used_part
BEFORE INSERT ON used_part
FOR EACH ROW
EXECUTE FUNCTION deduct_inventory();

-- =========================
-- 10. INDEX
-- =========================
CREATE INDEX idx_asset_status ON asset(status);
CREATE INDEX idx_asset_department ON asset(department_id);

CREATE INDEX idx_sr_status ON service_request(status);
CREATE INDEX idx_sr_asset ON service_request(asset_id);

CREATE INDEX idx_maintenance_asset ON maintenance_schedule(asset_id);

CREATE INDEX idx_inventory_quantity ON inventory(quantity);

-- =========================
-- 11. SEED DATA (OPTIONAL)
-- =========================
INSERT INTO role(name) VALUES
('ADMIN'),
('DOCTOR'),
('NURSE'),
('ENGINEER'),
('ACCOUNTANT'),
('MANAGER');
const entityConfigs = {
    authors: {
        endpoint: "/api/v1/authors",
        columns: ["id", "name"],
        fields: ["name"],
        normalize: (formData) => ({ name: formData.get("name").trim() })
    },
    books: {
        endpoint: "/api/v1/books",
        columns: ["id", "title", "author_id", "year"],
        fields: ["title", "author_id", "year"],
        normalize: (formData) => ({
            title: formData.get("title").trim(),
            author_id: Number(formData.get("author_id")),
            year: Number(formData.get("year"))
        })
    },
    members: {
        endpoint: "/api/v1/members",
        columns: ["id", "name"],
        fields: ["name"],
        normalize: (formData) => ({ name: formData.get("name").trim() })
    },
    loans: {
        endpoint: "/api/v1/loans",
        columns: ["id", "book_id", "member_id"],
        fields: ["book_id", "member_id"],
        normalize: (formData) => ({
            book_id: Number(formData.get("book_id")),
            member_id: Number(formData.get("member_id"))
        })
    }
};

const entityState = Object.fromEntries(
    Object.keys(entityConfigs).map((entity) => [entity, { page: 1, limit: 5 }])
);

document.addEventListener("DOMContentLoaded", () => {
    bindForms();
    bindToolbar();
    Object.keys(entityConfigs).forEach((entity) => loadEntity(entity));
});

function bindForms() {
    document.querySelectorAll(".entity-form").forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();
            const entity = form.dataset.entity;
            await saveEntity(entity, form);
        });

        form.querySelector(".reset-form-btn").addEventListener("click", () => resetForm(form));
    });
}

function bindToolbar() {
    document.querySelectorAll(".limit-select").forEach((select) => {
        select.addEventListener("change", () => {
            const entity = select.dataset.entity;
            entityState[entity].limit = Number(select.value);
            entityState[entity].page = 1;
            loadEntity(entity);
        });
    });

    document.querySelectorAll(".refresh-btn").forEach((button) => {
        button.addEventListener("click", () => loadEntity(button.dataset.entity));
    });
}

async function loadEntity(entity) {
    const { endpoint, columns } = entityConfigs[entity];
    const { page, limit } = entityState[entity];
    const offset = (page - 1) * limit;

    setStatus(entity, "Đang tải dữ liệu...", "");

    try {
        const response = await fetch(`${endpoint}?offset=${offset}&limit=${limit}`);
        const payload = await response.json();

        if (!response.ok) {
            throw new Error(payload.error || "Không thể tải dữ liệu");
        }

        const totalPages = Math.max(1, Math.ceil(payload.total / limit));
        if (page > totalPages) {
            entityState[entity].page = totalPages;
            return loadEntity(entity);
        }

        renderTable(entity, payload.data, columns);
        renderPagination(entity, payload.total, page, limit);
        setStatus(entity, `Đang hiển thị ${payload.data.length}/${payload.total} bản ghi`, "success");
    } catch (error) {
        renderTable(entity, [], columns);
        renderPagination(entity, 0, 1, limit);
        setStatus(entity, error.message, "error");
    }
}

function renderTable(entity, data, columns) {
    const tbody = document.getElementById(`${entity}-table-body`);
    tbody.innerHTML = "";

    if (!data.length) {
        const row = document.createElement("tr");
        row.innerHTML = `<td colspan="${columns.length + 1}">Không có dữ liệu.</td>`;
        tbody.appendChild(row);
        return;
    }

    data.forEach((item) => {
        const row = document.createElement("tr");
        const cells = columns.map((column) => `<td>${escapeHtml(item[column])}</td>`).join("");
        row.innerHTML = `
            ${cells}
            <td class="actions">
                <button type="button" class="ghost">Sửa</button>
                <button type="button" class="danger">Xóa</button>
            </td>
        `;

        const [editButton, deleteButton] = row.querySelectorAll("button");
        editButton.addEventListener("click", () => populateForm(entity, item));
        deleteButton.addEventListener("click", () => deleteEntity(entity, item.id));

        tbody.appendChild(row);
    });
}

function renderPagination(entity, total, currentPage, limit) {
    const pagination = document.getElementById(`${entity}-pagination`);
    const totalPages = Math.max(1, Math.ceil(total / limit));
    const safeCurrentPage = Math.min(currentPage, totalPages);
    entityState[entity].page = safeCurrentPage;

    pagination.innerHTML = "";

    const meta = document.createElement("span");
    meta.className = "pagination-meta";
    meta.textContent = `Trang ${safeCurrentPage}/${totalPages} | Limit ${limit}`;
    pagination.appendChild(meta);

    pagination.appendChild(
        createPageButton("Previous", safeCurrentPage === 1, () => changePage(entity, safeCurrentPage - 1))
    );

    for (let page = 1; page <= totalPages; page += 1) {
        const button = createPageButton(String(page), false, () => changePage(entity, page));
        button.classList.add("page-number");
        if (page === safeCurrentPage) {
            button.classList.add("active");
        }
        pagination.appendChild(button);
    }

    pagination.appendChild(
        createPageButton("Next", safeCurrentPage === totalPages, () => changePage(entity, safeCurrentPage + 1))
    );
}

function createPageButton(label, disabled, onClick) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.disabled = disabled;
    button.addEventListener("click", onClick);
    return button;
}

function changePage(entity, nextPage) {
    if (nextPage < 1) {
        return;
    }
    entityState[entity].page = nextPage;
    loadEntity(entity);
}

async function saveEntity(entity, form) {
    const config = entityConfigs[entity];
    const formData = new FormData(form);
    const id = formData.get("id");
    const payload = config.normalize(formData);

    setStatus(entity, "Đang lưu dữ liệu...", "");

    try {
        const response = await fetch(id ? `${config.endpoint}/${id}` : config.endpoint, {
            method: id ? "PUT" : "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Không thể lưu dữ liệu");
        }

        resetForm(form);
        setStatus(entity, id ? "Cập nhật thành công" : "Tạo mới thành công", "success");
        await loadEntity(entity);
    } catch (error) {
        setStatus(entity, error.message, "error");
    }
}

async function deleteEntity(entity, id) {
    const config = entityConfigs[entity];
    setStatus(entity, `Đang xóa bản ghi #${id}...`, "");

    try {
        const response = await fetch(`${config.endpoint}/${id}`, { method: "DELETE" });
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Không thể xóa dữ liệu");
        }

        await loadEntity(entity);
        setStatus(entity, result.message || "Xóa thành công", "success");
    } catch (error) {
        setStatus(entity, error.message, "error");
    }
}

function populateForm(entity, item) {
    const form = document.querySelector(`.entity-form[data-entity="${entity}"]`);
    form.elements.id.value = item.id;
    entityConfigs[entity].fields.forEach((field) => {
        form.elements[field].value = item[field];
    });
    form.scrollIntoView({ behavior: "smooth", block: "center" });
    setStatus(entity, `Đang chỉnh sửa bản ghi #${item.id}`, "");
}

function resetForm(form) {
    form.reset();
    form.elements.id.value = "";
}

function setStatus(entity, message, type) {
    const node = document.querySelector(`[data-entity-status="${entity}"]`);
    node.textContent = message;
    node.className = "status-message";
    if (type) {
        node.classList.add(type);
    }
}

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

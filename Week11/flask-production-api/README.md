# Flask Production API - Logging & Monitoring

Ứng dụng Flask đầy đủ với hệ thống logging, monitoring (Prometheus + Grafana) và rate limiting.

## 📋 Yêu cầu hệ thống

- Docker & Docker Compose
- Python 3.12 (nếu chạy local)
- Postman hoặc curl (để test API)
- Browser (để xem Grafana dashboard)

## 🚀 Khởi chạy ứng dụng

### 1. Chuẩn bị môi trường

```bash
# Di chuyển vào thư mục project
cd flask-production-api

# Tạo thư mục logs (nếu chưa tồn tại)
mkdir -p logs
```

### 2. Khởi chạy toàn bộ stack với Docker Compose

```bash
# Khởi chạy tất cả services (API + Prometheus + Grafana)
docker-compose up -d

# Hoặc rebuild lại image nếu có thay đổi
docker-compose up -d --build
```

### 3. Kiểm tra trạng thái services

```bash
# Xem status của tất cả containers
docker-compose ps

# Xem logs của API service
docker-compose logs -f api

# Xem logs của Prometheus
docker-compose logs prometheus

# Xem logs của Grafana
docker-compose logs grafana
```

## 🔧 Dừng ứng dụng

```bash
# Dừng tất cả services
docker-compose down

# Xóa volumes (cẩn thận - sẽ xóa dữ liệu)
docker-compose down -v
```

## 📊 Truy cập các thành phần

| Thành phần | URL | Mô tả |
|-----------|-----|-------|
| **API** | http://localhost:3000 | Flask API server |
| **Prometheus** | http://localhost:9090 | Metrics database |
| **Grafana** | http://localhost:3001 | Dashboard visualization |

## 🧪 Test các thành phần

### 1. Test API Endpoints

#### a) Health Check
```bash
curl -X GET http://localhost:3000/health
```

**Kết quả mong đợi:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

#### b) Home Endpoint
```bash
curl -X GET http://localhost:3000/
```

**Kết quả mong đợi:**
```json
{
  "message": "Flask Production API",
  "version": "1.0.0",
  "status": "running"
}
```

#### c) Get All Users (Rate limited: 10 requests/minute)
```bash
curl -X GET http://localhost:3000/api/users
```

**Kết quả mong đợi:**
```json
[
  {"id": 1, "name": "Alice", "email": "alice@example.com"},
  {"id": 2, "name": "Bob", "email": "bob@example.com"},
  {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
]
```

#### d) Get Specific User (Rate limited: 15 requests/minute)
```bash
curl -X GET http://localhost:3000/api/users/1
```

**Kết quả mong đợi:**
```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com"
}
```

### 2. Test Rate Limiting

#### Với curl - Test Rate Limit trên /api/users

```bash
# Chạy 15 request trong vòng 1 phút (limit: 10/phút)
for i in {1..15}; do
  echo "Request $i:"
  curl -X GET http://localhost:3000/api/users
  sleep 2  # Chờ 2 giây giữa các request
done
```

**Kết quả khi vượt quá giới hạn (HTTP 429):**
```json
{
  "error": "Rate limit exceeded",
  "message": "10 per 1 minute"
}
```

#### Với Postman

1. Mở Postman
2. Tạo request mới: `GET http://localhost:3000/api/users`
3. Click "Send" liên tục 11 lần trong vòng 1 phút
4. Request thứ 11 sẽ trả về status **429** với message rate limit

**Bước chi tiết:**
- URL: `http://localhost:3000/api/users`
- Method: `GET`
- Headers: (không cần)
- Body: (không cần)

### 3. Test Logging

#### Kiểm tra file logs
```bash
# Xem file log chính
cat logs/app.log

# Xem file log lỗi
cat logs/error.log

# Theo dõi logs real-time
tail -f logs/app.log
```

**Cấu trúc log:**
```
2024-05-13 10:30:45 - api_logger - INFO - [before_request:52] - [REQUEST] GET /api/users from 127.0.0.1
2024-05-13 10:30:45 - api_logger - INFO - [after_request:73] - [RESPONSE] GET /api/users - Status: 200
```

#### Xem logs từ Docker
```bash
# Logs của API service
docker-compose logs api --tail=50

# Theo dõi logs real-time
docker-compose logs -f api
```

### 4. Test Prometheus Metrics

#### a) Truy cập metrics endpoint
```bash
curl -X GET http://localhost:3000/metrics
```

**Sẽ hiển thị tất cả metrics dạng text format của Prometheus**

#### b) Truy cập Prometheus UI
- URL: http://localhost:9090
- Vào tab "Graph" hoặc "Table"
- Nhập query: `http_requests_total`
- Click "Execute"

**Các query hữu ích:**
```
# Tổng số requests
http_requests_total

# Request rate (5 phút)
rate(http_requests_total[5m])

# Active requests
http_requests_active

# Rate limit exceeded count
rate_limit_exceeded_total

# Average response time
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])
```

### 5. Test Grafana Dashboard

#### a) Đăng nhập Grafana
1. Truy cập: http://localhost:3001
2. Username: `admin`
3. Password: `admin`

#### b) Xem Dashboard
1. Nhấp vào menu (☰) ở top-left
2. Chọn "Dashboards"
3. Tìm "Flask API Monitoring Dashboard"
4. Dashboard sẽ hiển thị:
   - **Request Rate** (5 phút average)
   - **Total Requests by Endpoint**
   - **Average Response Time**
   - **Rate Limit Exceeded Rate**
   - **Active HTTP Requests**

#### c) Tạo Dashboard tùy chỉnh (nếu cần)
1. Nhấp "Create" → "Dashboard"
2. Nhấp "Add panel"
3. Chọn Prometheus data source
4. Nhập query, ví dụ: `http_requests_total`
5. Nhấp "Save"

## 📝 Workflow Test Hoàn Chỉnh

### Scenario: Kiểm tra toàn bộ hệ thống

```bash
# 1. Khởi chạy services
docker-compose up -d

# 2. Chờ ~10 giây để services khởi động hoàn toàn
sleep 10

# 3. Test API health
curl http://localhost:3000/health

# 4. Generate some traffic
for i in {1..20}; do
  curl -s http://localhost:3000/api/users > /dev/null
  curl -s http://localhost:3000/api/users/1 > /dev/null
  sleep 1
done

# 5. Kiểm tra logs
docker-compose logs api --tail=20

# 6. Xem metrics
curl -s http://localhost:3000/metrics | head -50

# 7. Truy cập Prometheus (http://localhost:9090)
#    - Query: rate(http_requests_total[5m])

# 8. Truy cập Grafana (http://localhost:3001)
#    - Login: admin/admin
#    - View Flask API Monitoring Dashboard
```

## 🔍 Troubleshooting

### Issue: Port đã được sử dụng

```bash
# Kiểm tra port
lsof -i :3000  # API
lsof -i :9090  # Prometheus
lsof -i :3001  # Grafana

# Nếu cần dùng port khác, sửa docker-compose.yml
```

### Issue: Grafana không hiển thị dữ liệu

1. Chờ ~30 giây để Prometheus thu thập dữ liệu
2. Kiểm tra Prometheus có connect được tới API không:
   - Truy cập http://localhost:9090/targets
   - Xem status của flask-api job

### Issue: Logs không xuất hiện

1. Kiểm tra thư mục `logs/` tồn tại
2. Kiểm tra permissions: `chmod 755 logs/`
3. Xem logs trong container: `docker-compose logs api`

### Issue: Rate limit không hoạt động

1. Kiểm tra các requests bằng Postman hoặc curl
2. Xem logs: `docker-compose logs api`
3. Xem endpoint có @limiter decorator không

## 📌 Các Endpoints Chính

| Endpoint | Method | Rate Limit | Mô tả |
|----------|--------|-----------|-------|
| `/` | GET | 100/hour | Home page |
| `/health` | GET | 100/hour | Health check |
| `/api/users` | GET | 10/minute | Lấy danh sách users |
| `/api/users/<id>` | GET | 15/minute | Lấy user cụ thể |
| `/metrics` | GET | - | Prometheus metrics |

## 📂 Cấu trúc Project

```
flask-production-api/
├── app/
│   ├── app.py              # Main Flask app
│   ├── logger.py           # Logging configuration
│   └── __init__.py
├── provisioning/
│   ├── datasources/
│   │   └── prometheus.yml  # Grafana datasource config
│   └── dashboards/
│       ├── dashboards.yml  # Dashboard provisioning
│       └── flask-api-dashboard.json
├── logs/                   # Log files directory
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Flask app container
├── prometheus.yml          # Prometheus configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔒 Security Notes

- Đổi password Grafana default: `admin/admin` → mật khẩu mạnh
- Sử dụng environment variables cho credentials
- Không commit sensitive data vào git
- Sử dụng HTTPS trong production

## 📈 Monitoring Metrics

Ứng dụng theo dõi:
- **Total HTTP Requests** - `http_requests_total`
- **Request Duration** - `http_request_duration_seconds`
- **Active Requests** - `http_requests_active`
- **Rate Limit Violations** - `rate_limit_exceeded_total`

## 🛠️ Phát triển thêm

### Thêm endpoint mới

```python
@app.route('/api/endpoint')
@limiter.limit("20 per minute")
def endpoint():
    logger.info("Endpoint called")
    return jsonify({"data": "value"}), 200
```

### Thay đổi rate limit

Sửa trong `app.py`:
```python
@limiter.limit("5 per minute")  # Thay đổi giới hạn ở đây
def users():
    ...
```

## 📚 Tài liệu tham khảo

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Flask-Limiter](https://flask-limiter.readthedocs.io/)
- [Prometheus Client Python](https://github.com/prometheus/client_python)

## 📞 Hỗ trợ

Nếu có vấn đề:
1. Kiểm tra logs: `docker-compose logs [service]`
2. Kiểm tra port: `lsof -i :[port]`
3. Restart services: `docker-compose restart`

---

**Last Updated:** May 2024
**Version:** 1.0.0

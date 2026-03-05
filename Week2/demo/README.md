# Users RESTful API

Một máy chủ REST API cho quản lý người dùng được xây dựng bằng Node.js và Express.

## Cài đặt

1. Cài đặt các phụ thuộc:
```bash
npm install
```

2. Khởi động máy chủ:
```bash
npm start
```

Hoặc dùng `npm run dev` để khởi động với nodemon (tự động reload):
```bash
npm run dev
```

Máy chủ sẽ chạy trên `http://localhost:3000`

## API Endpoints

### 1. Lấy tất cả người dùng
```
GET /api/users
```

200 (OK): Lấy danh sách thành công
500 (Internal Server Error): Lỗi đọc dữ liệu từ database

**Ví dụ Response:**
```json
[
  {
    "id": "1",
    "name": "Nguyễn Văn An",
    "email": "an.nguyen@example.com",
    "phoneNumber": "0901234567"
  }
]
```

### 2. Lấy người dùng theo ID
```
GET /api/users/:id
```

200 (OK): Tìm thấy người dùng
404 (Not Found): Người dùng không tồn tại
500 (Internal Server Error): Lỗi đọc dữ liệu

**Ví dụ:**
```
GET /api/users/1
```

### 3. Tạo người dùng mới
```
POST /api/users
Content-Type: application/json

201 (Created): Tạo người dùng thành công
400 (Bad Request): Thiếu name hoặc email
500 (Internal Server Error): Lỗi tạo người dùng

{
  "name": "Tên người dùng",
  "email": "email@example.com",
  "phoneNumber": "0123456789"
}
```

### 4. Cập nhật thông tin người dùng
```
PUT /api/users/:id
Content-Type: application/json

200 (OK): Cập nhật thành công
400 (Bad Request): Thiếu name hoặc email
404 (Not Found): Người dùng không tồn tại
500 (Internal Server Error): Lỗi cập nhật

{
  "name": "Tên mới",
  "email": "email_moi@example.com",
  "phoneNumber": "0987654321"
}
```

### 5. Xóa người dùng
```
DELETE /api/users/:id
```
200 (OK): Xóa thành công
404 (Not Found): Người dùng không tồn tại
500 (Internal Server Error): Lỗi xóa

### 6. Kiểm tra trạng thái server
```
GET /api/health
```

## Ví dụ sử dụng với cURL

### Lấy tất cả người dùng
```bash
curl http://localhost:3000/api/users
```

### Lấy người dùng có ID = 1
```bash
curl http://localhost:3000/api/users/1
```

### Tạo người dùng mới
```bash
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Trương Minh","email":"truong@example.com","phoneNumber":"0912345678"}'
```

### Cập nhật người dùng
```bash
curl -X PUT http://localhost:3000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Nguyễn Văn An Mới","email":"an_new@example.com"}'
```

### Xóa người dùng
```bash
curl -X DELETE http://localhost:3000/api/users/1
```

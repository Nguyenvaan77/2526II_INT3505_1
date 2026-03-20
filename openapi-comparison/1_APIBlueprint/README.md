# 1_APIBlueprint - Library Management API

## Mô tả

API Blueprint là một định dạng markdown cho phép tài liệu API dễ đọc và dễ bảo trì. Nó được thiết kế để dễ học và dễ viết.

## 📋 Tệp tin

- **blueprint.md** - Định nghĩa API theo chuẩn API Blueprint

## 🚀 Cài đặt và Chạy

### 1. Xem tài liệu API

#### Option A: Sử dụng Apiary Online
1. Truy cập: https://apiary.io/
2. Đăng nhập или tạo tài khoản miễn phí
3. Copy nội dung file `blueprint.md` vào editor
4. Xem tài liệu tương tác

#### Option B: Sử dụng Aglio (API Blueprint Renderer)

```bash
# 1. Cài đặt Aglio
npm install -g aglio

# 2. Tạo documentation HTML
aglio -i blueprint.md -o index.html

# 3. Mở trong trình duyệt
# Windows: start index.html
# Mac: open index.html
# Linux: xdg-open index.html
```

#### Option C: Sử dụng Dredd (API Blueprint Tester)

```bash
# 1. Cài đặt Dredd
npm install -g dredd

# 2. Test API specification
dredd blueprint.md http://localhost:3000
```

### 2. Mock Server từ API Blueprint

#### Sử dụng Prism Mock Server

```bash
# 1. Cài đặt Prism (hỗ trợ OpenAPI, Blueprint, v.v.)
npm install -g @stoplight/prism-cli

# 2. Tạo mock server từ blueprint
# Chuyển đổi blueprint sang OpenAPI trước
npm install -g api2swagger
api2swagger -u blueprint.md -o openapi-temp.yaml

# 3. Chạy mock server
prism mock openapi-temp.yaml -p 3001
```

#### Hoặc sử dụng DreddMock

```bash
# 1. Cài đặt dredds
npm install -g dreddmock

# 2. Chạy mock server
dreddmock blueprint.md
```

### 3. Validation

```bash
# 1. Cài đặt fury
npm install -g fury-cli

# 2. Validate specification
fury validate blueprint.md
```

### 4. Code Generation

#### Chuyển đổi sang OpenAPI rồi generate code

```bash
# 1. Cài đặt converter
npm install -g api2swagger

# 2. Chuyển đổi sang OpenAPI
api2swagger -u blueprint.md -o openapi.yaml

# 3. Sử dụng OpenAPI generator
openapi-generator-cli generate -i openapi.yaml -g nodejs-express-server -o ./generated/server
```

## 📝 Ưu điểm của API Blueprint

✅ Syntax giống Markdown, dễ đọc và dễ viết
✅ Tốt cho tài liệu có nội dung văn bản phong phú
✅ Dễ học cho người mới
✅ Hỗ trợ mock server và testing

## 📖 Tham khảo

- [API Blueprint Documentation](https://apiblueprint.org/)
- [Apiary - API Blueprint Hosting & Testing](https://apiary.io/)
- [Aglio - API Blueprint Renderer](https://github.com/danielgtaylor/aglio)
- [Dredd - API Testing Tool](https://dredd.org/)
- [Prism - API Mocking](https://stoplight.io/open-source/prism)

## 💡 Ví dụ Test API

```bash
# Khi mock server chạy tại localhost:3000

# Get all books
curl http://localhost:3000/books

# Get one book
curl http://localhost:3000/books/1

# Create book
curl -X POST http://localhost:3000/books \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Design Patterns",
    "author_name": "Gang of Four",
    "description": "Sách về các pattern lập trình"
  }'

# Update book
curl -X PUT http://localhost:3000/books/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Clean Code - Updated"}'

# Delete book
curl -X DELETE http://localhost:3000/books/1
```

## 🔧 Tính năng chính

1. **Dễ đọc**: Sử dụng markdown syntax quen thuộc
2. **Tài liệu phong phú**: Hỗ trợ mô tả chi tiết bằng text
3. **Mock Testing**: Dễ tạo mock server để test
4. **Conversible**: Dễ chuyển đổi sang OpenAPI
5. **Community**: Cộng đồng nhỏ nhưng đoàn kết

## 📝 So sánh với các định dạng khác

| Feature | Blueprint | OpenAPI | RAML | TypeSpec |
|---------|-----------|---------|------|----------|
| Dễ học | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Markdown-like | ⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ |
| Công cụ hỗ trợ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Code generation | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

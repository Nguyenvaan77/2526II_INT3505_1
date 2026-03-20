# 2_RAML - Library Management API

## Mô tả

RAML (RESTful API Modeling Language) là một ngôn ngữ dựa trên YAML để mô tả các REST APIs. Nó cung cấp một cách cấu trúc để định nghĩa các resource, method, parameter và response.

## 📋 Tệp tin

- **library.raml** - Định nghĩa API theo chuẩn RAML 1.0

## 🚀 Cài đặt và Chạy

### 1. Xem tài liệu API

#### Option A: Sử dụng RAML Browser Online
1. Truy cập: https://raml.org/projects/projects
2. Hoặc: https://mulesoft.github.io/raml-for-jax-rs/raml-home.html
3. Copy nội dung file `library.raml` vào

#### Option B: Cài đặt API Workbench (VS Code)
1. Cài đặt VS Code extension: **API Workbench**
2. Mở file `library.raml` trong VS Code
3. Nhấn `Alt + P` để xem preview
4. Sử dụng **RAML Console** để test API

#### Option C: Sử dụng RAMLParser

```bash
# 1. Cài đặt RAML parser
npm install -g raml2obj

# 2. Chuyển đổi sang HTML documentation
raml2obj library.raml -o library.html

# 3. Mở trong trình duyệt
# Windows: start library.html
```

### 2. Code Generation từ RAML

#### Sử dụng Mule Code Generator

```bash
# 1. Cài đặt Mule tools
npm install -g raml2jaxrs

# 2. Generate Java server từ RAML
raml2jaxrs library.raml -o ./generated/java-server

# 3. Generate Node.js server
npm install -g raml-for-nodejs
raml-for-nodejs library.raml -o ./generated/nodejs-server
```

#### Sử dụng RAML to OpenAPI Converter

```bash
# 1. Cài đặt converter
npm install -g api2swagger

# 2. Chuyển RAML sang OpenAPI
# Lưu ý: API2Swagger hỗ trợ hiệu quả OpenAPI, RAML conversion có thể cần công cụ khác
npm install -g oas-raml-converter

# 3. Nếu cần, chuyển sang OpenAPI trước
```

### 3. Validation

```bash
# 1. Cài đặt API Workbench hoặc RAML validator
npm install -g raml-parser

# 2. Validate RAML file
raml-parser library.raml
```

### 4. Mock Server từ RAML

#### Sử dụng Prism (Universal Mock Server)

```bash
# 1. Cài đặt Prism
npm install -g @stoplight/prism-cli

# 2. Chạy mock server từ RAML
# Prism hỗ trợ OpenAPI, nhưng có thể chuyển RAML sang OpenAPI trước
# Hoặc sử dụng RAM console tích hợp
```

#### Sử dụng API Designer (Mulesoft Online)

1. Truy cập: https://www.mulesoft.com/platform/api/anypoint
2. Upload file `library.raml`
3. Sử dụng RAML Console built-in để mock

### 5. Testing

```bash
# Sử dụng curl hoặc Postman để test
# (Khi mock server chạy)

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

## 📝 Ưu điểm của RAML

✅ YAML dễ đọc
✅ Hỗ trợ reusable types và resources
✅ Tốt cho API lớn và phức tạp
✅ Có hỗ trợ để tái sử dụng components

## 📖 Tham khảo

- [RAML Official Documentation](https://raml.org/)
- [API Workbench (VS Code Extension)](https://github.com/mulesoft-labs/api-workbench)
- [RAML Parser](https://github.com/raml-org/raml-js-parser)
- [Mulesoft API Designer](https://www.mulesoft.com/platform/api/anypoint)

## 🔧 Tính năng chính

1. **Reusable Components**: Định nghĩa một lần, sử dụng nhiều lần
2. **Resource Hierarchy**: Dễ dàng xác định relationship giữa resources
3. **Type System**: Mạnh mẽ với object, array, enum types
4. **Traits**: Hỗ trợ DRY (Don't Repeat Yourself) principle
5. **Security Schemes**: Hỗ trợ OAuth, Basic Auth, API Key

## 💡 Ví dụ Traits (DRY Principle)

```yaml
traits:
  paged:
    queryParameters:
      skip:
        type: integer
        default: 0
      limit:
        type: integer
        default: 10

/books:
  get:
    is: [paged]  # Reuse paged trait
```

## 📝 So sánh với các định dạng khác

| Feature | RAML | OpenAPI | Blueprint | TypeSpec |
|---------|------|---------|-----------|----------|
| Đọc hiểu | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Reusable Components | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Code generation | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Công cụ hỗ trợ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Cộng đồng | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

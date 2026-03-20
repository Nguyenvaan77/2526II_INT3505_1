# 3_TypeSpec - Library Management API

## Mô tả

TypeSpec (trước đây gọi là Cadl) là một ngôn ngữ định nghĩa API mới được phát triển bởi Microsoft. Nó được thiết kế để dễ sử dụng cho các developer quen thuộc với TypeScript/JavaScript.

## 📋 Tệp tin

- **library.tsp** - Định nghĩa API theo chuẩn TypeSpec

## 🚀 Cài đặt và Chạy

### 1. Cài đặt TypeSpec

#### Yêu cầu
- Node.js >= 18.0.0
- npm hoặc yarn

#### Cài đặt

```bash
# 1. Cài đặt TypeSpec compiler
npm install -g @typespec/compiler

# 2. Cài đặt TypeSpec libraries
npm install -g @typespec/http @typespec/rest @typespec/openapi3
```

### 2. Xem tài liệu API (Tạo OpenAPI từ TypeSpec)

```bash
# 1. Tạo thư mục project
mkdir typespec-project
cd typespec-project

# 2. Khởi tạo TypeSpec project
tsp init

# 3. Copy file library.tsp vào

# 4. Compile TypeSpec sang OpenAPI
tsp compile . --emit @typespec/openapi3

# 5. Xem file generated openapi.yaml
# Sau đó, sử dụng Swagger UI hoặc công cụ khác để xem tài liệu
```

### 3. Sử dụng TypeSpec VS Code Extension

1. Cài đặt VS Code extension: **TypeSpec for VS Code**
2. Mở file `library.tsp`
3. Extension sẽ tự động hiển thị preview
4. Nhấn `Ctrl+Shift+P` > "TypeSpec: Show output" để xem output

### 4. Code Generation từ TypeSpec

#### Generate OpenAPI

```bash
# TypeSpec có thể generate sang OpenAPI 3.0
tsp compile . --emit @typespec/openapi3

# File sẽ được lưu tại ./tsp-output/openapi.yaml
```

#### Generate từ OpenAPI (Python, Node.js, Java, v.v.)

```bash
# 1. Sau khi generate OpenAPI, sử dụng OpenAPI Generator
openapi-generator-cli generate -i ./tsp-output/openapi.yaml -g nodejs-express-server -o ./generated/nodejs

# 2. Hoặc generate Python
openapi-generator-cli generate -i ./tsp-output/openapi.yaml -g python -o ./generated/python

# 3. Hoặc generate Java
openapi-generator-cli generate -i ./tsp-output/openapi.yaml -g java -o ./generated/java
```

### 5. Mock Server từ TypeSpec

```bash
# 1. Cài đặt Prism CLI
npm install -g @stoplight/prism-cli

# 2. Generate OpenAPI từ TypeSpec
tsp compile . --emit @typespec/openapi3

# 3. Chạy mock server
prism mock ./tsp-output/openapi.yaml -p 3000
```

### 6. Validation

```bash
# 1. TypeSpec compiler tự động validate
tsp compile .

# 2. Nếu không có lỗi, spec hợp lệ
```

## 📝 Ưu điểm của TypeSpec

✅ Sử dụng TypeScript syntax, quen thuộc với developers
✅ Có thể generate sang OpenAPI, RAML, JSON Schema
✅ Syntax gọn gàng, dễ đọc
✅ Strong type support
✅ Extensions mạnh mẽ với decorators

## 📖 Tham khảo

- [TypeSpec Official Documentation](https://microsoft.github.io/typespec/)
- [TypeSpec GitHub Repository](https://github.com/microsoft/typespec)
- [TypeSpec VS Code Extension](https://marketplace.visualstudio.com/items?itemName=Microsoft.typespec)
- [TypeSpec Playground](https://microsoft.github.io/typespec/)

## 🔧 Tính năng chính

1. **TypeScript-like Syntax**: Familiar cho JS/TS developers
2. **Decorators**: @doc, @format, @minLength, v.v.
3. **Union Types**: Hỗ trợ multiple responses (200 | 400 | 500)
4. **Reusable Models**: Dễ tái sử dụng định nghĩa
5. **Strong Validation**: Compile-time validation

## 💡 Ví dụ Decorators

```typescript
@doc("Tên sách")                    // Documentation
@minLength(1)                       // Validation rule
@maxLength(255)                     // Validation rule
name: string;
```

## 📝 So sánh với các định dạng khác

| Feature | TypeSpec | OpenAPI | Blueprint | RAML |
|---------|----------|---------|-----------|------|
| Syntax | TypeScript | YAML | Markdown | YAML |
| Dễ học | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Type support | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Code generation | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Công cụ hỗ trợ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Cộng đồng | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

## 🚀 Kết luận

TypeSpec là một lựa chọn tuyệt vời nếu:
- Team quen thuộc với TypeScript/JavaScript
- Cần một tiêu chuẩn mới, có sự hỗ trợ từ Microsoft
- Muốn syntax gọn gàng và dễ đọc
- Cần generate sang nhiều format khác nhau

## 💡 Ví dụ Chạy Nhanh

```bash
# 1. Tạo file main.tsp
# 2. Thêm nội dung TypeSpec
# 3. Chạy compiler
tsp compile . --emit @typespec/openapi3

# 4. Xem generated openapi.yaml
cat tsp-output/openapi.yaml

# 5. Chạy mock server
prism mock tsp-output/openapi.yaml -p 3000

# 6. Test API
curl http://localhost:3000/books
```

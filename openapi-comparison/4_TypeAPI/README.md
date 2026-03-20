# 4_TypeAPI (OpenAPI 3.0) - Library Management API

## Mô tả

OpenAPI 3.0 (trước đây gọi là Swagger) là tiêu chuẩn công nghiệp để mô tả các REST APIs. File `openapi.yaml` chứa định nghĩa hoàn chỉnh về Library Management API.

## 📋 Tệp tin

- **openapi.yaml** - Định nghĩa API theo tiêu chuẩn OpenAPI 3.0

## 🚀 Cài đặt và Chạy

### 1. Xem tài liệu API (Swagger UI)

#### Option A: Sử dụng Swagger Editor Online
1. Truy cập: https://editor.swagger.io/
2. Copy nội dung file `openapi.yaml` vào editor
3. Xem tài liệu và thử các endpoint

#### Option B: Cài đặt Swagger UI locally

```bash
# 1. Cài đặt thư viện
npm install -g swagger-ui-express express

# 2. Tạo file server.js
```

Tạo file `server.js` trong thư mục này:

```javascript
const express = require('express');
const swaggerUi = require('swagger-ui-express');
const fs = require('fs');
const yaml = require('js-yaml');

const app = express();

// Đọc file OpenAPI
const openapiFile = fs.readFileSync('./openapi.yaml', 'utf8');
const swaggerDefinition = yaml.load(openapiFile);

// Setup Swagger UI
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDefinition));

// Mock API implementation
app.use(express.json());

const books = [
  { id: '1', name: 'Clean Code', author_name: 'Robert C. Martin', description: 'Hướng dẫn viết code sạch' }
];

// Get all books
app.get('/books', (req, res) => {
  const { skip = 0, limit = 10 } = req.query;
  res.json({
    data: books.slice(skip, skip + limit),
    total: books.length,
    skip: parseInt(skip),
    limit: parseInt(limit)
  });
});

// Get one book
app.get('/books/:id', (req, res) => {
  const book = books.find(b => b.id === req.params.id);
  if (!book) return res.status(404).json({ error: 'Book not found' });
  res.json({ data: book });
});

// Create book
app.post('/books', (req, res) => {
  const { name, author_name, description } = req.body;
  if (!name || !author_name || !description) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  const newBook = {
    id: String(Date.now()),
    name,
    author_name,
    description,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };
  books.push(newBook);
  res.status(201).json({ data: newBook, message: 'Book created successfully' });
});

// Update book
app.put('/books/:id', (req, res) => {
  const book = books.find(b => b.id === req.params.id);
  if (!book) return res.status(404).json({ error: 'Book not found' });
  
  Object.assign(book, req.body);
  book.updated_at = new Date().toISOString();
  res.json({ data: book, message: 'Book updated successfully' });
});

// Delete book
app.delete('/books/:id', (req, res) => {
  const index = books.findIndex(b => b.id === req.params.id);
  if (index === -1) return res.status(404).json({ error: 'Book not found' });
  
  books.splice(index, 1);
  res.json({ message: 'Book deleted successfully' });
});

app.listen(3000, () => {
  console.log('Server running at http://localhost:3000');
  console.log('Swagger UI at http://localhost:3000/api-docs');
});
```

Chạy:
```bash
node server.js
```

Truy cập: http://localhost:3000/api-docs

### 2. Code Generation từ OpenAPI

#### Sử dụng OpenAPI Generator

```bash
# 1. Cài đặt OpenAPI Generator
npm install -g @openapitools/openapi-generator-cli

# 2. Generate Python client
openapi-generator-cli generate -i openapi.yaml -g python -o ./generated/python-client

# 3. Generate Node.js server
openapi-generator-cli generate -i openapi.yaml -g nodejs-express-server -o ./generated/nodejs-server

# 4. Generate TypeScript client
openapi-generator-cli generate -i openapi.yaml -g typescript-fetch -o ./generated/ts-client
```

#### Sử dụng Swagger Codegen

```bash
# 1. Download swagger-codegen
swagger-codegen generate -i openapi.yaml -l python -o ./generated/python-client

# 2. Generate Java client
swagger-codegen generate -i openapi.yaml -l java -o ./generated/java-client
```

### 3. Validation

```bash
# Cài đặt swagger-parser
npm install swagger-parser

# Validate specification
swagger-parser validate openapi.yaml
```

## 📝 Ưu điểm của OpenAPI

✅ Tiêu chuẩn công nghiệp, được hỗ trợ rộng rãi
✅ Đầy đủ công cụ hỗ trợ (Swagger UI, codegen)
✅ Hỗ trợ các loại xác thực phức tạp
✅ Dễ tích hợp với CI/CD
✅ Cộng đồng lớn

## 📖 Tham khảo

- [OpenAPI Specification](https://spec.openapis.org/oas/v3.0.3)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [OpenAPI Generator](https://openapi-generator.tech/)
- [Swagger Editor](https://editor.swagger.io/)

## 💡 Ví dụ Test API

```bash
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

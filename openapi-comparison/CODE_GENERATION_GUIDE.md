# Code Generation from API Documentation Formats

> **Folder Mapping:**
> - OpenAPI 3.0: `4_TypeAPI/openapi.yaml`
> - API Blueprint: `1_APIBlueprint/blueprint.md`
> - RAML: `2_RAML/library.raml`
> - TypeSpec: `3_TypeSpec/library.tsp`

## 📚 Tổng quan

Code generation là quá trình tự động tạo mã nguồn (client, server, models, tests) từ các tệp tài liệu API. Điều này giúp:

- ✅ Giảm lỗi manual coding
- ✅ Giữ code và documentation luôn đồng bộ
- ✅ Tiết kiệm thời gian phát triển
- ✅ Đảm bảo consistency trong codebase

## 🔄 Quy trình Code Generation

```
API Specification (OpenAPI/RAML/Blueprint/TypeSpec)
           ↓
    [Parser/Validator]
           ↓
        AST/Model
           ↓
    [Code Generator]
           ↓
Generated Code (Client/Server/Models/Tests)
```

---

## 1. CODE GENERATION từ OpenAPI

### A. Generate Python Client

```bash
# Cài đặt OpenAPI Generator
npm install -g @openapitools/openapi-generator-cli

# Generate Python client
openapi-generator-cli generate \
  -i ./4_TypeAPI/openapi.yaml \
  -g python \
  -o ./generated/python-client \
  --package-name library_api

# Cài đặt generated client
cd generated/python-client
pip install -e .

# Sử dụng
from library_api.apis.books_api import BooksAPI
from library_api.models.book import Book

client = BooksAPI()
books = client.get_all_books()
```

### B. Generate Node.js TypeScript Client

```bash
# Generate TypeScript client
openapi-generator-cli generate \
  -i ./4_TypeAPI/openapi.yaml \
  -g typescript-fetch \
  -o ./generated/ts-client

# Cài đặt dependencies
cd generated/ts-client
npm install

# Sử dụng
import { BooksAPI } from './generated/apis';

const api = new BooksAPI();
const books = await api.getAllBooks();
```

### C. Generate Node.js Express Server

```bash
# Generate server skeleton
openapi-generator-cli generate \
  -i ./4_TypeAPI/openapi.yaml \
  -g nodejs-express-server \
  -o ./generated/nodejs-server

cd generated/nodejs-server
npm install

# Chạy server
npm start
```

### D. Generate Java Client

```bash
openapi-generator-cli generate \
  -i ./4_TypeAPI/openapi.yaml \
  -g java \
  -o ./generated/java-client \
  --package-name com.library.api

# Hoặc build Maven project
cd generated/java-client
mvn clean install
```

### E. Generate C# .NET Client

```bash
openapi-generator-cli generate \
  -i ./4_TypeAPI/openapi.yaml \
  -g csharp-netcore \
  -o ./generated/csharp-client

cd generated/csharp-client
dotnet build
```

### F. Generate Go Client

```bash
openapi-generator-cli generate \
  -i ./4_TypeAPI/openapi.yaml \
  -g go \
  -o ./generated/go-client
```

### G. Generate Postman Collection

```bash
openapi-generator-cli generate \
  -i ./4_TypeAPI/openapi.yaml \
  -g postman-collection \
  -o ./generated/postman

# Import vào Postman:
# Postman > Import > Select generated collection.json
```

### H. Generate API Documentation (HTML)

```bash
# Cài đặt Swagger UI
npm install -g swagger-ui-express

# Hoặc sử dụng ReDoc
npm install -g redoc-cli

# Tạo HTML documentation
redoc-cli build 4_TypeAPI/openapi.yaml -o openapi-docs.html
```

---

## 2. CODE GENERATION từ RAML

### A. Chuyển RAML sang OpenAPI (rồi generate)

```bash
# Cài đặt converter
npm install -g oas-raml-converter

# Chuyển RAML sang OpenAPI
raml2oas raml/library.raml --output openapi-from-raml.yaml

# Sau đó sử dụng OpenAPI generator
openapi-generator-cli generate \
  -i openapi-from-raml.yaml \
  -g python \
  -o ./generated/from-raml-python
```

### B. Generate trực tiếp từ RAML

```bash
# Sử dụng Mule tools
npm install -g raml-for-nodejs

raml-for-nodejs raml/library.raml -o ./generated/raml-nodejs
```

### C. Generate Java từ RAML

```bash
npm install -g raml2jaxrs

raml2jaxrs raml/library.raml -o ./generated/raml-java
```

---

## 3. CODE GENERATION từ API Blueprint

### A. Chuyển API Blueprint sang OpenAPI

```bash
# Cài đặt converter
npm install -g api2swagger

# Chuyển sang OpenAPI
api2swagger -u api-blueprint/blueprint.md -o blueprint-as-openapi.yaml

# Sau đó generate code
openapi-generator-cli generate \
  -i blueprint-as-openapi.yaml \
  -g python \
  -o ./generated/from-blueprint-python
```

### B. Generate Mock Server từ Blueprint

```bash
# Cài đặt Prism
npm install -g @stoplight/prism-cli

# Chạy mock server
prism mock api-blueprint/blueprint.md -p 3001
```

### C. Testen API Blueprint với Dredd

```bash
# Cài đặt Dredd
npm install -g dredd

# Test specification
dredd api-blueprint/blueprint.md http://localhost:3000
```

---

## 4. CODE GENERATION từ TypeSpec

### A. Generate OpenAPI từ TypeSpec

```bash
# Cài đặt TypeSpec
npm install -g @typespec/compiler @typespec/http @typespec/openapi3

# Tạo thư mục project
mkdir typespec-project
cd typespec-project

# Copy library.tsp vào

# Generate OpenAPI
tsp compile . --emit @typespec/openapi3

# OpenAPI sẽ ở tsp-output/openapi.yaml
```

### B. Generate Client từ TypeSpec-generated OpenAPI

```bash
# Sau khi generate OpenAPI
openapi-generator-cli generate \
  -i tsp-output/openapi.yaml \
  -g typescript-fetch \
  -o ./generated/ts-from-typespec
```

### C. Generate Mock Server từ TypeSpec

```bash
# Sau khi generate OpenAPI
prism mock tsp-output/openapi.yaml -p 3000
```

### D. Generate JSON Schema từ TypeSpec

```bash
# TypeSpec cũng có thể generate JSON Schema
tsp compile . --emit @typespec/json-schema
```

---

## 5. Ví dụ THỰC TẾ - End-to-End Code Generation

### Scenario: Tạo Python client từ OpenAPI

```bash
# 1. Generate Python client
openapi-generator-cli generate \
  -i ./openapi/openapi.yaml \
  -g python \
  -o ./generated/python-client \
  --package-name library_api

# 2. Cài đặt
cd generated/python-client
pip install -e .

# 3. Tạo script test
```

**test_generated_client.py:**
```python
from library_api.apis.books_api import BooksAPI
from library_api.models.book import Book
from library_api.models.create_book_request import CreateBookRequest

# Setup
api = BooksAPI()
api.api_client.host = "http://localhost:3000"

# Get all books
books = api.get_all_books()
print(f"Books: {books}")

# Create book
new_book = CreateBookRequest(
    name="New Book",
    author_name="John Doe",
    description="A great book"
)
created = api.create_book(new_book)
print(f"Created: {created}")

# Get one book
book = api.get_book(created.id)
print(f"Retrieved: {book}")

# Update book
book.name = "Updated Name"
updated = api.update_book(created.id, book)
print(f"Updated: {updated}")

# Delete book
api.delete_book(created.id)
print("Deleted")
```

### Scenario: Tạo TypeScript client từ OpenAPI

```bash
# 1. Generate TypeScript client
openapi-generator-cli generate \
  -i ./openapi/openapi.yaml \
  -g typescript-fetch \
  -o ./generated/ts-client

# 2. Cài đặt
cd generated/ts-client
npm install

# 3. Tạo script test
```

**test_generated_client.ts:**
```typescript
import { BooksAPI, CreateBookRequest } from './generated';

const api = new BooksAPI({
  basePath: 'http://localhost:3000'
});

// Get all books
const books = await api.getAllBooks();
console.log('Books:', books);

// Create book
const newBook: CreateBookRequest = {
  name: 'New Book',
  author_name: 'Jane Doe',
  description: 'Amazing book'
};
const created = await api.createBook(newBook);
console.log('Created:', created);

// Get one book
const book = await api.getBook(created.id);
console.log('Retrieved:', book);

// Update book
book.name = 'Updated Name';
const updated = await api.updateBook(created.id, book);
console.log('Updated:', updated);

// Delete book
await api.deleteBook(created.id);
console.log('Deleted');
```

---

## 6. So sánh Code Generation Support

| Format | Python | Node.js | Java | C# | Go | Postman |
|--------|--------|---------|------|----|----|---------|
| **OpenAPI** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **RAML** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Blueprint** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **TypeSpec** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 7. Best Practices

### ✅ Do's
- Generate từ một source of truth (spec file)
- Commit generated code vào version control
- Tự động loại bỏ old generated folder trước khi generate lại
- Sử dụng CI/CD để tự động generate khi spec thay đổi
- Test generated code

### ❌ Don'ts
- Không edit generated code trực tiếp (chỉnh sửa spec rồi re-generate)
- Không sử dụng multiple spec formats cùng một lúc
- Không bỏ qua validation errors

---

## 8. Công cụ và Tài nguyên

- **OpenAPI Generator**: https://openapi-generator.tech/
- **Swagger Codegen**: https://swagger.io/tools/swagger-codegen/
- **RAML Tools**: https://raml.org/projects
- **API Blueprint Tools**: https://apiblueprint.org/
- **TypeSpec Compiler**: https://microsoft.github.io/typespec/
- **Prism Mock Server**: https://stoplight.io/open-source/prism

---

## 🎯 Kết luận

Chọn format với code generation support tốt nhất theo nhu cầu:

1. **OpenAPI** - Tốt nhất cho code generation, hỗ trợ rộng rãi
2. **TypeSpec** - Mới nhất, code generation mạnh mẽ
3. **RAML** - Code generation tốt cho API phức tạp
4. **API Blueprint** - Hỗ trợ code generation yếu hơn, nhưng dễ viết

**Khuyến nghị**: Sử dụng **OpenAPI** cho code generation, **TypeSpec** cho future-proof solutions!

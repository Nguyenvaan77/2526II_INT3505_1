# 📚 Library Management API - API Documentation Formats Comparison

## 🎯 Dự án

Ứng dụng quản lý thư viện mini với **5 endpoints cơ bản** (CRUD), được tài liệu hóa và triển khai bằng **4 format tài liệu API** khác nhau:
- **OpenAPI 3.0**
- **API Blueprint**
- **RAML 1.0**
- **TypeSpec**

## 📋 Cấu trúc Thư mục

```
openapi-comparison/
├── 4_TypeAPI (OpenAPI 3.0)
│   ├── openapi.yaml          # OpenAPI 3.0 specification
│   ├── README.md             # Hướng dẫn OpenAPI
│
├── 1_APIBlueprint
│   ├── blueprint.md          # API Blueprint specification
│   ├── README.md             # Hướng dẫn API Blueprint
│
├── 2_RAML
│   ├── library.raml          # RAML 1.0 specification
│   ├── README.md             # Hướng dẫn RAML
│
├── 3_TypeSpec
│   ├── library.tsp           # TypeSpec specification
│   ├── README.md             # Hướng dẫn TypeSpec
│
├── app.py                    # Flask implementation (supports all formats)
├── test_api.py              # Comprehensive test suite
├── requirements.txt         # Python dependencies
├── CODE_GENERATION_GUIDE.md # Chi tiết code generation
├── README.md                # (Đây) Tổng quan dự án
└── setup.sh                 # Setup script for quick start
```

## 🚀 Cài đặt Nhanh

### 1. Cài đặt Python Dependencies

```bash
# Windows
pip install -r requirements.txt

# Linux/Mac
pip3 install -r requirements.txt
```

### 2. Chạy Server

```bash
# Terminal 1
python app.py
# hoặc
python3 app.py

# Server sẽ chạy tại http://localhost:3000
```

### 3. Test API (Terminal khác)

```bash
# Terminal 2
python test_api.py
# hoặc
python3 test_api.py
```

## 📚 5 Endpoints API

| Endpoint | Method | Mô tả | Status |
|----------|--------|-------|--------|
| `/books` | GET | Lấy danh sách tất cả sách | ✅ |
| `/books` | POST | Tạo sách mới | ✅ |
| `/books/{id}` | GET | Lấy thông tin một sách | ✅ |
| `/books/{id}` | PUT | Cập nhật sách | ✅ |
| `/books/{id}` | DELETE | Xóa sách | ✅ |

### Book Model

```json
{
  "id": "string (UUID)",
  "name": "string (required, 1-255 chars)",
  "author_name": "string (required, 1-255 chars)",
  "description": "string (required, max 1000 chars)",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime"
}
```

## 🔄 4 Format Tài liệu API - So sánh

### 1️⃣ OpenAPI 3.0 (4_TypeAPI)
**Vị trí**: `4_TypeAPI/openapi.yaml`

- ✅ Tiêu chuẩn công nghiệp, được OpenAPI Initiative quản lý
- ✅ Hỗ trợ code generation tốt nhất
- ✅ Công cụ: Swagger UI, Swagger Editor, OpenAPI Generator
- ✅ Cộng đồng lớn nhất

**Khi nào dùng**: Đa số các dự án, đặc biệt API lớn

**Sinh code**: Python, Node.js, Java, C#, Go, Postman, v.v.

### 2️⃣ API Blueprint (1_APIBlueprint)
**Vị trí**: `1_APIBlueprint/blueprint.md`

- ✅ Syntax giống Markdown, dễ đọc
- ✅ Tốt cho tài liệu có nội dung văn bản phong phú
- ✅ Công cụ: Apiary, Aglio, Dredd
- ⚠️ Cộng đồng nhỏ hơn

**Khi nào dùng**: Team muốn documentation dễ đọc, integrations, webhooks

**Sinh code**: Hỗ trợ trung bình, dùng chuyển đổi sang OpenAPI

### 3️⃣ RAML 1.0 (2_RAML)
**Vị trí**: `2_RAML/library.raml`

- ✅ YAML dễ đọc, cấu trúc rõ ràng
- ✅ Hỗ trợ reusable types và traits
- ✅ Công cụ: Mulesoft API Designer, API Workbench
- ⚠️ Ít được sử dụng trong các dự án mới

**Khi nào dùng**: API phức tạp cần reusable components

**Sinh code**: RAML to OpenAPI, rồi generate

### 4️⃣ TypeSpec (3_TypeSpec)
**Vị trí**: `3_TypeSpec/library.tsp`

- ✅ Sử dụng TypeScript syntax, quen thuộc với dev
- ✅ Code generation mạnh mẽ
- ✅ Phát triển bởi Microsoft
- ✅ Có thể generate sang OpenAPI, RAML, JSON Schema

**Khi nào dùng**: Dự án mới, team TypeScript-focused, future-proof

**Sinh code**: OpenAPI, rồi generate sang Python, Node.js, Java, v.v.

---

## 📖 Cách Xem/Chạy Từng Format

### 4_TypeAPI (OpenAPI 3.0)

```bash
# Option 1: Online Swagger Editor
# Truy cập: https://editor.swagger.io/
# Copy nội dung openapi/openapi.yaml

# Option 2: Local Swagger UI (cần Node.js)
npm install -g swagger-ui-express
# [Follow README trong openapi/ folder]

# Option 3: ReDoc
npm install -g redoc-cli
redoc-cli bundle openapi/openapi.yaml -o openapi-docs.html
open openapi-docs.html
```

### 1_APIBlueprint (API Blueprint)

```bash
# Option 1: Online Apiary
# Truy cập: https://apiary.io/
# Copy nội dung api-blueprint/blueprint.md

# Option 2: Local Aglio
npm install -g aglio
aglio -i api-blueprint/blueprint.md -o blueprint-docs.html
open blueprint-docs.html

# Option 3: Dredd Testing
npm install -g dredd
dredd api-blueprint/blueprint.md http://localhost:3000
```

### 2_RAML (RAML 1.0)

```bash
# Option 1: API Workbench (VS Code Extension)
# Cài đặt: "API Workbench" extension
# Mở: raml/library.raml
# Nhấn: Alt + P để xem preview

# Option 2: Online API Designer
# Truy cập: https://raml.org/projects
# Upload raml/library.raml

# Option 3: RAML to OpenAPI
npm install -g oas-raml-converter
raml-to-openapi raml/library.raml --output temp-openapi.yaml
```

### 3_TypeSpec (TypeSpec)

```bash
# Cài đặt TypeSpec
npm install -g @typespec/compiler @typespec/http @typespec/openapi3

# Tạo project folder
mkdir typespec-demo
cd typespec-demo

# Copy library.tsp

# Generate OpenAPI
tsp compile . --emit @typespec/openapi3

# Xem tệp generated
cat tsp-output/openapi.yaml
```

---

## 🧪 Testing API

### Cách 1: Dùng Test Script Python (Khuyến nghị)

```bash
# Terminal 1
python app.py

# Terminal 2
python test_api.py
```

Sẽ chạy 10 test cases:
- ✅ Get all books
- ✅ Get with pagination
- ✅ Get with sorting
- ✅ Create book
- ✅ Create with invalid data
- ✅ Get single book
- ✅ Get non-existent book (404)
- ✅ Update book
- ✅ Delete book
- ✅ Delete non-existent book (404)

### Cách 2: Dùng cURL

```bash
# Server chạy tại localhost:3000

# Get all
curl http://localhost:3000/books

# Get one
curl http://localhost:3000/books/1

# Create
curl -X POST http://localhost:3000/books \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Book",
    "author_name": "Author Name",
    "description": "Book description"
  }'

# Update
curl -X PUT http://localhost:3000/books/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'

# Delete
curl -X DELETE http://localhost:3000/books/1
```

### Cách 3: Dùng Postman

1. Mở Postman
2. Nhập URL: `http://localhost:3000/books`
3. Chọn method (GET, POST, PUT, DELETE)
4. Nhập request body (JSON)
5. Click Send

---

## 🔧 Code Generation từ API Specs

Chi tiết lệnh code generation xem: **CODE_GENERATION_GUIDE.md**

### Quick Examples

#### Generate Python Client từ OpenAPI

```bash
npm install -g @openapitools/openapi-generator-cli

openapi-generator-cli generate \
  -i 4_TypeAPI/openapi.yaml \
  -g python \
  -o generated/python-client \
  --package-name library_api
```

#### Generate TypeScript Client từ OpenAPI

```bash
openapi-generator-cli generate \
  -i 4_TypeAPI/openapi.yaml \
  -g typescript-fetch \
  -o generated/ts-client
```

#### Generate Node.js Server từ OpenAPI

```bash
openapi-generator-cli generate \
  -i 4_TypeAPI/openapi.yaml \
  -g nodejs-express-server \
  -o generated/nodejs-server
```

#### Generate từ TypeSpec

```bash
npm install -g @typespec/compiler @typespec/openapi3

cd 3_TypeSpec/
tsp compile . --emit @typespec/openapi3

# Sau đó generate từ tsp-output/openapi.yaml
```

---

## 📊 So sánh Chi Tiết

Bảng so sánh đầy đủ xem: **README.md** (root openapi-comparison folder)

| Tiêu chí | OpenAPI | Blueprint | RAML | TypeSpec |
|---------|---------|-----------|------|----------|
| **Dễ học** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Công cụ** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Code Gen** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Cộng đồng** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Khuyến nghị** | ✅✅✅ | ✅✅ | ✅✅ | ✅✅✅ |

---

## 🎓 Học Tập

### Documentation Formats
1. **OpenAPI**: https://spec.openapis.org/oas/v3.0.3
2. **API Blueprint**: https://apiblueprint.org/
3. **RAML**: https://raml.org/
4. **TypeSpec**: https://microsoft.github.io/typespec/

### Code Generation
- **OpenAPI Generator**: https://openapi-generator.tech/
- **Swagger Codegen**: https://swagger.io/tools/swagger-codegen/
- **Tools List**: Xem CODE_GENERATION_GUIDE.md

### Công cụ Hỗ trợ
- **Swagger UI**: https://swagger.io/tools/swagger-ui/
- **Postman**: https://www.postman.com/
- **Apiary**: https://apiary.io/
- **Stoplight Studio**: https://stoplight.io/studio/

---

## 💡 Best Practices

### ✅ DO
- Viết spec trước khi viết code
- Sử dụng code generation để giảm boilerplate
- Giữ spec và code đồng bộ
- Test API qua tài liệu
- Version control spec file

### ❌ DON'T
- Không edit generated code (sửa spec rồi re-gen)
- Không mix multiple spec formats
- Không bỏ qua validation
- Không generate mà không test

---

## 🚀 Khuyến Nghị Sử Dụng

| Tình huống | Khuyến nghị | Lý do |
|-----------|-----------|-------|
| **Dự án mới, không biết chọn gì** | OpenAPI | Chuẩn công nghiệp, tools tốt nhất |
| **Team quen TypeScript** | TypeSpec | Modern, familiar syntax |
| **API rất phức tạp, lớn** | RAML | Reusable components support |
| **Muốn docs shmartly dễ đọc** | API Blueprint | Markdown-like, readable |
| **Cần mock server nhanh** | API Blueprint + Dredd | Dễ setup |
| **Enterprise solution** | OpenAPI | Hỗ trợ, tooling tốt |
| **Microservices** | OpenAPI | Dễ integrate vào CI/CD |

---

## 📝 Bài Tập

1. **Thêm endpoint mới** → Cập nhật tất cả 4 format
2. **Sinh code Python từ từng format** → So sánh kết quả
3. **Tạo mock server từ mỗi format** → Test endpoints
4. **Viết integration test** → Đảm bảo API hoạt động

---

## 🤝 Đóng Góp

Để thêm features:
1. Update API spec (chọn 1 hoặc cả 4 format)
2. Re-generate code từ spec
3. Implement logic
4. Test

---

## 📞 Hỗ trợ

Cho mỗi format, xem README trong folder riêng:
- `openapi/README.md` - OpenAPI hướng dẫn chi tiết
- `api-blueprint/README.md` - API Blueprint hướng dẫn
- `raml/README.md` - RAML hướng dẫn
- `typespec/README.md` - TypeSpec hướng dẫn

---

## 📄 License

MIT License

---

## ✨ Tóm Tắt

```
API Spec (4 Formats)
    ↓
Mock Server / Validator
    ↓
Code Generation
    ↓
Client/Server Implementation
    ↓
Testing & Documentation
    ↓
Production Ready API
```

**Điểm mạnh của "spec-first" approach:**
1. 📚 Tài liệu luôn cập nhật (from spec)
2. 🔄 Code generation giảm lỗi
3. 🧪 Dễ test (spec defines behavior)
4. 🤝 Dễ collaboration (spec là source of truth)
5. 🚀 Tăng tốc độ development

---

**Happy API Documentation! 🎉**

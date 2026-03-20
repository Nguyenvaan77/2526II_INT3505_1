# API Documentation Formats Comparison

## Ứng dụng: Quản lý Thư viện Mini (Library Management)

Ứng dụng quản lý sách với các trường cơ bản:
- **name**: Tên sách
- **author_name**: Tên tác giả
- **description**: Mô tả

### 5 Endpoints cơ bản:
1. **GET /books** - Lấy danh sách tất cả sách
2. **GET /books/{id}** - Lấy thông tin một cuốn sách
3. **POST /books** - Tạo sách mới
4. **PUT /books/{id}** - Cập nhật thông tin sách
5. **DELETE /books/{id}** - Xóa sách

---

## So sánh 4 Format Tài liệu API

| Tiêu chí | OpenAPI 3.0 | API Blueprint | RAML 1.0 | TypeSpec |
|---------|------------|---------------|---------|----------|
| **Năm phát hành** | 2017 | 2013 | 2013 | 2023 |
| **Định dạng** | YAML / JSON | Markdown | YAML | TypeScript |
| **Dễ học** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Công cụ hỗ trợ** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Code Generation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Validation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Cộng đồng** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

### 1. **OpenAPI 3.0** (Formerly Swagger)
- **Ưu điểm:**
  - Tiêu chuẩn công nghiệp, được hỗ trợ rộng rãi
  - Đầy đủ công cụ hỗ trợ (Swagger UI, codegen)
  - Hỗ trợ các loại xác thực phức tạp
  - Dễ tích hợp với CI/CD
  
- **Nhược điểm:**
  - YAML/JSON có thể dài dòng
  - Đường cong học tập một chút cao

### 2. **API Blueprint**
- **Ưu điểm:**
  - Syntax như Markdown, dễ đọc
  - Tốt cho tài liệu có nội dung văn bản phong phú
  - Dễ viết và dễ hiểu cho người mới

- **Nhược điểm:**
  - Ít công cụ hỗ trợ hơn OpenAPI
  - Cộng đồng nhỏ hơn
  - Kém linh hoạt cho API phức tạp

### 3. **RAML 1.0** (RESTful API Modeling Language)
- **Ưu điểm:**
  - YAML dễ đọc
  - Hỗ trợ reusable types và resources
  - Tốt cho các API lớn và phức tạp

- **Nhược điểm:**
  - Thiếu công cụ code generation mạnh mẽ
  - Cộng đồng nhỏ hơn OpenAPI
  - Ít được sử dụng trong các dự án mới

### 4. **TypeSpec** (Mới nhất)
- **Ưu điểm:**
  - Sử dụng TypeScript, quen thuộc với dev
  - Code generation mạnh mẽ
  - Có thể tạo ra OpenAPI, RAML từ TypeSpec
  - Hỗ trợ validation tốt

- **Nhược điểm:**
  - Công cụ và cộng đồng còn thiếu so với OpenAPI
  - Phải cài đặt Node.js

---

## Cấu trúc Thư mục

```
openapi-comparison/
├── 4_TypeAPI (OpenAPI 3.0)      # OpenAPI 3.0 format
│   ├── openapi.yaml            # OpenAPI specification
│   └── README.md               # Hướng dẫn cài đặt và chạy
│
├── 1_APIBlueprint              # API Blueprint format
│   ├── blueprint.md            # API Blueprint specification
│   └── README.md               # Hướng dẫn cài đặt và chạy
│
├── 2_RAML                      # RAML 1.0 format
│   ├── library.raml            # RAML specification
│   └── README.md               # Hướng dẫn cài đặt và chạy
│
├── 3_TypeSpec                  # TypeSpec format
│   ├── library.tsp             # TypeSpec specification
│   └── README.md               # Hướng dẫn cài đặt và chạy
│
├── app.py                      # Flask server implementation
├── test_api.py                # Comprehensive API tests
├── requirements.txt           # Python dependencies
├── setup.sh                   # Quick setup script
├── RUNNING_GUIDE.md           # Chi tiết cách chạy mọi thứ
├── CODE_GENERATION_GUIDE.md  # Chi tiết code generation
└── README.md                  # File này - Tổng quan so sánh
```

---

## Lợi ích của Code Generation

1. **Giảm lỗi:** Tự động tạo mã từ spec giảm lỗi manual coding
2. **Đồng bộ:** Mã và tài liệu luôn đồng bộ
3. **Tiết kiệm thời gian:** Không cần viết code boilerplate
4. **Thống nhất:** Đảm bảo format consistent trong team

---

## 🚀 Cách Chạy Nhanh

### 1. Cài đặt
```bash
pip install -r requirements.txt
```

### 2. Chạy Server
```bash
python app.py
# Server chạy tại http://localhost:3000
```

### 3. Test API (Terminal khác)
```bash
python test_api.py
```

📖 **Chi tiết:** Xem [RUNNING_GUIDE.md](RUNNING_GUIDE.md)

---

## 🔧 Code Generation

Chi tiết code generation từ các format xem: [CODE_GENERATION_GUIDE.md](CODE_GENERATION_GUIDE.md)

### Quick Examples:
```bash
# Generate Python client từ OpenAPI
openapi-generator-cli generate -i 4_TypeAPI/openapi.yaml -g python -o generated/python

# Generate TypeScript client từ OpenAPI
openapi-generator-cli generate -i 4_TypeAPI/openapi.yaml -g typescript-fetch -o generated/ts

# Generate Node.js server từ OpenAPI
openapi-generator-cli generate -i 4_TypeAPI/openapi.yaml -g nodejs-express-server -o generated/nodejs
```

---

## 🧪 Testing

Dùng test suite Python tích hợp:
```bash
python test_api.py
```

Hoặc dùng curl:
```bash
# Get all books
curl http://localhost:3000/books

# Create book
curl -X POST http://localhost:3000/books \
  -H "Content-Type: application/json" \
  -d '{"name":"Book","author_name":"Author","description":"Desc"}'
```

---

## 📖 Xem Tài liệu Từng Format

| Format | Folder | Cách xem | Hướng dẫn |
|--------|--------|---------|---------|
| **OpenAPI** | 4_TypeAPI/ | Swagger Editor (online) hoặc Swagger UI | [4_TypeAPI/README.md](4_TypeAPI/README.md) |
| **API Blueprint** | 1_APIBlueprint/ | Apiary (online) hoặc Aglio | [1_APIBlueprint/README.md](1_APIBlueprint/README.md) |
| **RAML** | 2_RAML/ | API Workbench (VS Code) hoặc Mulesoft | [2_RAML/README.md](2_RAML/README.md) |
| **TypeSpec** | 3_TypeSpec/ | VS Code Extension hoặc Compiler | [3_TypeSpec/README.md](3_TypeSpec/README.md) |

---

## 📚 Tài liệu Bổ sung

- [RUNNING_GUIDE.md](RUNNING_GUIDE.md) - Hướng dẫn chi tiết chạy từng format
- [CODE_GENERATION_GUIDE.md](CODE_GENERATION_GUIDE.md) - Chi tiết code generation

---

## Kết luận

- **OpenAPI (4_TypeAPI)**: Phù hợp cho hầu hết các dự án, đặc biệt những API lớn
  - ✅ Tiêu chuẩn công nghiệp
  - ✅ Code generation tốt nhất
  - ✅ Cộng đồng lớn
  
- **API Blueprint (1_APIBlueprint)**: Tốt cho team muốn tài liệu dễ đọc, giống Markdown
  - ✅ Markdown-like syntax
  - ✅ Dễ học
  - ⚠️ Cộng đồng nhỏ
  
- **RAML (2_RAML)**: Tốt cho API phức tạp cần reusable components
  - ✅ Reusable traits
  - ✅ YAML structure
  - ⚠️ Ít được sử dụng
  
- **TypeSpec (3_TypeSpec)**: Tương lai, đặc biệt nếu team quen TypeScript
  - ✅ Modern, TypeScript-based
  - ✅ Code generation mạnh
  - ✅ Hỗ trợ Microsoft

**💡 Khuyến nghị**: Bắt đầu với **OpenAPI 3.0 (4_TypeAPI)** nếu chưa chắc chắn!

---

**📌 Để nộp bài:** Gửi link folder `openapi-comparison` hoặc commit vào repository!

# 🚀 Quick Start Guide

## ⚡ 5 Phút Setup

### 1️⃣ Cài đặt Dependencies (1 phút)
```bash
pip install -r requirements.txt
```

### 2️⃣ Chạy Server (Terminal 1)
```bash
python app.py
```
**Output:** 
```
🚀 Library Management API Server
📚 Starting on http://localhost:3000
```

### 3️⃣ Test API (Terminal 2)
```bash
python test_api.py
```
**Output:** ✅ 10 test cases passed

---

## 📚 Xem Tài Liệu

### OpenAPI
1. Truy cập: https://editor.swagger.io/
2. Copy nội dung từ `openapi/openapi.yaml`
3. Dán vào editor

### API Blueprint
1. Truy cập: https://apiary.io/
2. Copy nội dung từ `api-blueprint/blueprint.md`
3. Dán vào web editor

### RAML
1. Cài đặt VS Code extension: "API Workbench"
2. Mở `raml/library.raml`
3. Nhấn `Alt + P` để xem preview

### TypeSpec
1. Cài đặt: `npm install -g @typespec/compiler @typespec/http @typespec/openapi3`
2. Chạy: `cd typespec && tsp compile . --emit @typespec/openapi3`
3. Xem: `tsp-output/openapi.yaml` (OpenAPI version)

---

## 🧪 Test với cURL

```bash
# Get all books
curl http://localhost:3000/books

# Get one book
curl http://localhost:3000/books/1

# Create book
curl -X POST http://localhost:3000/books \
  -H "Content-Type: application/json" \
  -d '{"name":"Book","author_name":"Author","description":"Desc"}'

# Update book
curl -X PUT http://localhost:3000/books/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"New Name"}'

# Delete book
curl -X DELETE http://localhost:3000/books/1
```

---

## 🔧 Code Generation (Quick)

### Generate Python Client từ OpenAPI
```bash
npm install -g @openapitools/openapi-generator-cli

openapi-generator-cli generate \
  -i 4_TypeAPI/openapi.yaml \
  -g python \
  -o generated/python-client \
  --package-name library_api
```

### Generate TypeScript Client
```bash
openapi-generator-cli generate \
  -i 4_TypeAPI/openapi.yaml \
  -g typescript-fetch \
  -o generated/ts-client
```

---

## 📖 Tệp Documents

| File | Purpose |
|------|---------|
| `README.md` | So sánh 4 format |
| `RUNNING_GUIDE.md` | Chi tiết cách chạy |
| `CODE_GENERATION_GUIDE.md` | Code generation |
| `PROJECT_SUMMARY.md` | Project overview |
| `QUICKSTART.md` | File này - nhanh nhất |

---

## 🎯 5 Endpoints

| Endpoint | Method | Status |
|----------|--------|--------|
| `/books` | GET | ✅ |
| `/books` | POST | ✅ |
| `/books/{id}` | GET | ✅ |
| `/books/{id}` | PUT | ✅ |
| `/books/{id}` | DELETE | ✅ |

---

## 🟢 Status

- ✅ OpenAPI 3.0 spec
- ✅ API Blueprint spec
- ✅ RAML spec
- ✅ TypeSpec spec
- ✅ Flask server implementation
- ✅ Comprehensive tests
- ✅ Code generation guide
- ✅ Running guide

---

## ❓ Troubleshooting

**Server không chạy?**
- Kiểm tra port 3000 đã bị chiếm?
- Chạy: `netstat -an | grep 3000`

**Tests không chạy?**
- Kiểm tra server đang chạy? (Terminal 1)
- Cài đặt requests: `pip install requests`

**TypeSpec không biên dịch?**
- Cài đặt Compiler: `npm install -g @typespec/compiler @typespec/http @typespec/openapi3`

---

## 💡 Tiếp Theo

1. Đọc `README.md` để hiểu về 4 format
2. Chạy `python app.py` + `python test_api.py`
3. Xem tài liệu từng format
4. Thử code generation
5. So sánh và chọn format yêu thích

---

**Happy API Learning! 🎉**

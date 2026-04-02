# RESTful API Documentation

## Cấu trúc Project

```
app.py - Entry point của ứng dụng Flask
data.py - Dữ liệu mock
pagination.py - Các hàm pagination
model/
  domain/ - Các class domain model (Author, Book, Member, Loan, Address)
  request/ - Các DTO request (AuthorRequest, BookRequest, MemberRequest, LoanRequest, AddressRequest)
  response/ - Các hàm transform response
routes/
  v1_routes.py - API v1 (Offset Pagination)
  v2_routes.py - API v2 (Page Pagination)
  v3_routes.py - API v3 (Cursor Pagination)
services/
  author_service.py - Business logic cho Author
  book_service.py - Business logic cho Book
  member_service.py - Business logic cho Member
  loan_service.py - Business logic cho Loan
  address_service.py - Business logic cho Address
```

## Kiến trúc Service-Based

Mỗi API request được xử lý theo flow:
1. **Route (Controller)** - Nhận request, validate dữ liệu
2. **Request DTO** - Chuyển JSON thành request object
3. **Service** - Xử lý business logic, truy cập data
4. **Response DTO** - Transform dữ liệu thành response object
5. **Route** - Trả về JSON response cho client

## API Endpoints

### API v1 - Offset Pagination (http://localhost:5000/api/v1)

#### AUTHOR APIs
- **GET /authors** - Lấy danh sách tác giả (phân trang offset)
  - Query: `offset=0&limit=5`
  - Response: Danh sách tác giả với metadata pagination
  
- **GET /authors/{id}** - Lấy tác giả theo ID
  
- **POST /authors** - Tạo tác giả mới
  - Body: `{"name": "string"}`
  - Response: HTTP 201 + tác giả mới
  
- **PUT /authors/{id}** - Cập nhật tác giả
  - Body: `{"name": "string"}`
  
- **DELETE /authors/{id}** - Xóa tác giả
  - Response: HTTP 200 nếu thành công, 404 nếu không tìm thấy

#### BOOK APIs
- **GET /books** - Lấy danh sách sách
- **GET /books/{id}** - Lấy sách theo ID
- **POST /books** - Tạo sách mới
  - Body: `{"title": "string", "author_id": int, "year": int}`
- **PUT /books/{id}** - Cập nhật sách
  - Body: `{"title": "string", "author_id": int, "year": int}` (tất cả optional)
- **DELETE /books/{id}** - Xóa sách

#### MEMBER APIs
- **GET /members** - Lấy danh sách thành viên
- **GET /members/{id}** - Lấy thành viên theo ID
- **POST /members** - Tạo thành viên mới
  - Body: `{"name": "string"}`
- **PUT /members/{id}** - Cập nhật thành viên
- **DELETE /members/{id}** - Xóa thành viên

#### LOAN APIs
- **GET /loans** - Lấy danh sách khoản mượn
- **GET /loans/{id}** - Lấy khoản mượn theo ID
- **POST /loans** - Tạo khoản mượn mới
  - Body: `{"book_id": int, "member_id": int}`
  - Validation: Kiểm tra book_id và member_id có tồn tại
- **PUT /loans/{id}** - Cập nhật khoản mượn
- **DELETE /loans/{id}** - Xóa khoản mượn

#### ADDRESS APIs
- **GET /addresses** - Lấy danh sách địa chỉ
  - Query: `author_id=1` (optional - filter theo tác giả)
- **GET /addresses/{id}** - Lấy địa chỉ theo ID
- **GET /authors/{author_id}/addresses** - Lấy tất cả địa chỉ của tác giả
- **GET /authors/{author_id}/addresses/{address_id}** - Lấy địa chỉ cụ thể của tác giả
- **POST /addresses** - Tạo địa chỉ mới
  - Body: `{"author_id": int, "city": "string", "country": "string"}`
  - Validation: Kiểm tra author_id có tồn tại
- **PUT /addresses/{id}** - Cập nhật địa chỉ
  - Body: `{"city": "string", "country": "string"}` (optional)
- **DELETE /addresses/{id}** - Xóa địa chỉ

### API v2 - Page Pagination (http://localhost:5000/api/v2)

Giống API v1 nhưng chỉ có GET endpoints với page-based pagination:
- Query: `page=1&size=5`
- Endpoints: `/authors`, `/books`, `/members`, `/loans`

### API v3 - Cursor Pagination (http://localhost:5000/api/v3)

Giống API v1 nhưng chỉ có GET endpoints với cursor-based pagination:
- Query: `cursor=1&limit=5`
- Endpoints: `/authors`, `/books`, `/members`, `/loans`

## Response Format

### Success Response (2xx)
```json
{
  "id": 1,
  "name": "George Orwell",
  "...": "..."
}
```

### Paginated Response
```json
{
  "offset": 0,
  "limit": 5,
  "total": 10,
  "data": [
    {"id": 1, "name": "..."},
    {"id": 2, "name": "..."}
  ]
}
```

### Error Response (4xx, 5xx)
```json
{
  "error": "Error message"
}
```

## Request/Response DTOs

### Author
- **Request (Create/Update)**: CreateAuthorRequest, UpdateAuthorRequest
  - Fields: name (string)
- **Response**: author_response(), author_detail_response(with addresses)

### Book
- **Request (Create/Update)**: CreateBookRequest, UpdateBookRequest
  - Fields: title, author_id, year (int)
- **Response**: book_response(), book_detail_response(with author)

### Member
- **Request (Create/Update)**: CreateMemberRequest, UpdateMemberRequest
  - Fields: name (string)
- **Response**: member_response()

### Loan
- **Request (Create/Update)**: CreateLoanRequest, UpdateLoanRequest
  - Fields: book_id, member_id
- **Response**: loan_response(), loan_detail_response(with book, member)

### Address
- **Request (Create/Update)**: CreateAddressRequest, UpdateAddressRequest
  - Fields: author_id, city, country
- **Response**: address_response(), address_detail_response(with author)

## Services

Mỗi service cung cấp các method:
- `get_all_*()` - Lấy tất cả
- `get_*_by_id(id)` - Lấy theo ID
- `get_*_with_*()` - Lấy với related data
- `create_*(request)` - Tạo mới từ request object
- `update_*(id, request)` - Cập nhật từ request object
- `delete_*(id)` - Xóa

Services xử lý:
- Business logic
- Validation dữ liệu
- Truy cập và cập nhật data
- Xử lý quan hệ giữa entities

## Error Handling

- **400 Bad Request**: Dữ liệu không hợp lệ (missing fields, invalid types)
- **404 Not Found**: Resource không tồn tại
- **201 Created**: Tạo resource thành công
- **200 OK**: Thao tác thành công

## Testing APIs

### Với cURL:
```bash
# GET
curl http://localhost:5000/api/v1/authors

# POST
curl -X POST http://localhost:5000/api/v1/authors \
  -H "Content-Type: application/json" \
  -d '{"name": "New Author"}'

# PUT
curl -X PUT http://localhost:5000/api/v1/authors/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Author"}'

# DELETE
curl -X DELETE http://localhost:5000/api/v1/authors/1
```

### Với Postman:
1. Import các endpoints vào Postman
2. Set request method (GET, POST, PUT, DELETE)
3. Set request body (JSON) cho POST/PUT
4. Send request

## Mở rộng trong tương lai

Có thể thêm:
- Database persistence (SQL, MongoDB)
- Authentication/Authorization (JWT, OAuth2)
- Request validation (marshmallow, pydantic)
- Logging và monitoring
- Unit tests
- API documentation (Swagger/OpenAPI)
- Rate limiting
- Caching

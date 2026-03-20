# Library Management API
## API Blueprint for Library Management System

### Description

Một ứng dụng quản lý thư viện mini cho phép quản lý sách với các thông tin cơ bản.

---

## API Information

- **Host:** `localhost:3000`
- **Base Path:** `/`
- **Schemes:** HTTP
- **Version:** 1.0.0

---

## Data Structures

### Book (object)
- **id** (string, required) - ID duy nhất của sách - `"1"`
- **name** (string, required) - Tên sách - `"Lập trình Python cơ bản"`
- **author_name** (string, required) - Tên tác giả - `"Nguyễn Văn A"`
- **description** (string, required) - Mô tả sách - `"Cuốn sách hướng dẫn lập trình Python"`
- **created_at** (string, optional) - Thời gian tạo (ISO 8601) - `"2024-01-15T10:30:00Z"`
- **updated_at** (string, optional) - Thời gian cập nhật - `"2024-01-20T15:45:00Z"`

### Books Collection (array)
Array of Book objects

### Error (object)
- **error** (string) - Thông báo lỗi
- **status** (integer) - HTTP status code
- **details** (array, optional) - Chi tiết lỗi

---

## Books Collection [/books]

### List All Books [GET]

Lấy danh sách tất cả sách trong thư viện.

+ Parameters
    + skip: 0 (integer, optional) - Số sách bỏ qua (pagination)
    + limit: 10 (integer, optional) - Số sách trả về (mặc định 10, tối thiểu 1)
    + sort_by: `created_at` (enum[string], optional) - Sắp xếp theo trường
        + Members
            + `name`
            + `author_name`
            + `created_at`

+ Response 200 (application/json)

    + Attributes (object)
        + data (array[Book])
        + total: 25 (number) - Tổng số sách
        + skip: 0 (number)
        + limit: 10 (number)

    + Body

            {
              "data": [
                {
                  "id": "1",
                  "name": "Clean Code",
                  "author_name": "Robert C. Martin",
                  "description": "Hướng dẫn viết code sạch",
                  "created_at": "2024-01-15T10:30:00Z",
                  "updated_at": "2024-01-20T15:45:00Z"
                },
                {
                  "id": "2",
                  "name": "Design Patterns",
                  "author_name": "Gang of Four",
                  "description": "Sách về các design pattern",
                  "created_at": "2024-01-16T11:00:00Z",
                  "updated_at": "2024-01-21T16:00:00Z"
                }
              ],
              "total": 25,
              "skip": 0,
              "limit": 10
            }

+ Response 500 (application/json)
    + Attributes (Error)

    + Body

            {
              "error": "Internal server error",
              "status": 500
            }

### Create a New Book [POST]

Tạo một cuốn sách mới trong thư viện.

+ Request (application/json)

    + Attributes (object)
        + name: "Game of Thrones" (string, required) - Tên sách
        + author_name: "George R. R. Martin" (string, required) - Tên tác giả
        + description: "Tiểu thuyết sử thi phương Tây" (string, required) - Mô tả sách

    + Body

            {
              "name": "Game of Thrones",
              "author_name": "George R. R. Martin",
              "description": "Tiểu thuyết sử thi phương Tây kì vĩ"
            }

+ Response 201 (application/json)

    + Attributes (object)
        + data (Book)
        + message: "Book created successfully" (string)

    + Body

            {
              "data": {
                "id": "1705318200000",
                "name": "Game of Thrones",
                "author_name": "George R. R. Martin",
                "description": "Tiểu thuyết sử thi phương Tây kì vĩ",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
              },
              "message": "Book created successfully"
            }

+ Response 400 (application/json)
    + Attributes (Error)

    + Body

            {
              "error": "Invalid request",
              "status": 400,
              "details": [
                "name is required",
                "author_name is required"
              ]
            }

+ Response 500 (application/json)
    + Attributes (Error)

---

## Book Detail [/books/{id}]

+ Parameters
    + id: `1` (string, required) - ID duy nhất của sách

### Get a Book [GET]

Lấy thông tin chi tiết của một cuốn sách theo ID.

+ Response 200 (application/json)

    + Attributes (object)
        + data (Book)

    + Body

            {
              "data": {
                "id": "1",
                "name": "Clean Code",
                "author_name": "Robert C. Martin",
                "description": "Hướng dẫn viết code sạch",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-20T15:45:00Z"
              }
            }

+ Response 404 (application/json)
    + Attributes (Error)

    + Body

            {
              "error": "Book not found",
              "status": 404
            }

+ Response 500 (application/json)
    + Attributes (Error)

### Update a Book [PUT]

Cập nhật thông tin của một cuốn sách theo ID.

+ Request (application/json)

    + Attributes (object)
        + name: "Clean Code - Updated Edition" (string, optional)
        + author_name: "Robert C. Martin" (string, optional)
        + description: "Hướng dẫn viết code sạch - Phiên bản cập nhật" (string, optional)

    + Body

            {
              "name": "Clean Code - Updated Edition",
              "description": "Hướng dẫn viết code sạch - Phiên bản cập nhật"
            }

+ Response 200 (application/json)

    + Attributes (object)
        + data (Book)
        + message: "Book updated successfully" (string)

    + Body

            {
              "data": {
                "id": "1",
                "name": "Clean Code - Updated Edition",
                "author_name": "Robert C. Martin",
                "description": "Hướng dẫn viết code sạch - Phiên bản cập nhật",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-20T15:45:00Z"
              },
              "message": "Book updated successfully"
            }

+ Response 400 (application/json)
    + Attributes (Error)

+ Response 404 (application/json)
    + Attributes (Error)

+ Response 500 (application/json)
    + Attributes (Error)

### Delete a Book [DELETE]

Xóa một cuốn sách từ thư viện theo ID.

+ Response 200 (application/json)

    + Attributes (object)
        + message: "Book deleted successfully" (string)

    + Body

            {
              "message": "Book deleted successfully"
            }

+ Response 404 (application/json)
    + Attributes (Error)

+ Response 500 (application/json)
    + Attributes (Error)

import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi3";

using TypeSpec.Http;
using TypeSpec.Rest;

@service(#{
  title: "Library Management API"
})
@doc("Library Management API - Version 1.0.0")
@server("http://localhost:3000", "Development server")
@server("http://localhost:5000", "Production server")
namespace LibraryAPI;

/**
 * Đối tượng sách
 */
model Book {
  @doc("ID duy nhất của sách")
  @format("uuid")
  id: string;

  @doc("Tên sách")
  @minLength(1)
  @maxLength(255)
  name: string;

  @doc("Tên tác giả")
  @minLength(1)
  @maxLength(255)
  author_name: string;

  @doc("Mô tả sách")
  @maxLength(1000)
  description: string;

  @doc("Thời gian tạo")
  created_at: utcDateTime;

  @doc("Thời gian cập nhật")
  updated_at: utcDateTime;
}

/**
 * Request tạo sách
 */
model CreateBookRequest {
  @minLength(1)
  @maxLength(255)
  name: string;

  @minLength(1)
  @maxLength(255)
  author_name: string;

  @minLength(1)
  @maxLength(1000)
  description: string;
}

/**
 * Request cập nhật sách
 */
model UpdateBookRequest {
  @minLength(1)
  @maxLength(255)
  name?: string;

  @minLength(1)
  @maxLength(255)
  author_name?: string;

  @maxLength(1000)
  description?: string;
}

/**
 * Pagination parameters
 */
model PaginationParams {
  @query
  @minValue(0)
  skip?: int32 = 0;

  @query
  @minValue(1)
  limit?: int32 = 10;

  @query
  sort_by?: "name" | "author_name" | "created_at" = "created_at";
}

/**
 * Response danh sách sách
 */
model BookListResponse {
  data: Book[];
  total: int32;
  skip: int32;
  limit: int32;
}

/**
 * Response sách
 */
model BookResponse {
  data: Book;
  message: string;
}

/**
 * Response xóa
 */
model DeleteResponse {
  message: string;
}

/**
 * Response lỗi
 */
model ErrorResponse {
  error: string;
  status: int32;
  details?: string[];
}

/**
 * API quản lý sách
 */
@route("/books")
interface BooksAPI {

  @doc("Lấy danh sách sách")
  @get
  getAllBooks(params: PaginationParams): {
    @statusCode _: 200;
    @body body: BookListResponse;
  } | {
    @statusCode _: 500;
    @body body: ErrorResponse;
  };

  @doc("Tạo sách mới")
  @post
  createBook(@body request: CreateBookRequest): {
    @statusCode _: 201;
    @body body: BookResponse;
  } | {
    @statusCode _: 400;
    @body body: ErrorResponse;
  };

  @doc("Lấy thông tin sách theo ID")
  @get
  @route("/{id}")
  getBook(@path id: string): {
    @statusCode _: 200;
    @body body: BookResponse;
  } | {
    @statusCode _: 404;
    @body body: ErrorResponse;
  };

  @doc("Cập nhật sách")
  @put
  @route("/{id}")
  updateBook(@path id: string, @body request: UpdateBookRequest): {
    @statusCode _: 200;
    @body body: BookResponse;
  } | {
    @statusCode _: 404;
    @body body: ErrorResponse;
  };

  @doc("Xóa sách")
  @delete
  @route("/{id}")
  deleteBook(@path id: string): {
    @statusCode _: 200;
    @body body: DeleteResponse;
  } | {
    @statusCode _: 404;
    @body body: ErrorResponse;
  };
}
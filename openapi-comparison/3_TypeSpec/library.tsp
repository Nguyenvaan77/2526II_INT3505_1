import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi3";

using TypeSpec.Http;
using TypeSpec.Rest;
using TypeSpec.OpenAPI;

@service({
  title: "Library Management API",
  version: "1.0.0",
})
@doc("Một ứng dụng quản lý thư viện mini cho phép quản lý sách với các thông tin cơ bản.")
@server("http://localhost:3000", "Development server")
@server("http://localhost:5000", "Production server")
namespace LibraryAPI;

/**
 * Đối tượng sách trong thư viện
 * Chứa các thông tin cơ bản về sách
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

  @doc("Thời gian tạo (ISO 8601)")
  created_at: utcDateTime;

  @doc("Thời gian cập nhật cuối cùng (ISO 8601)")
  updated_at: utcDateTime;
}

/**
 * Request để tạo sách mới
 */
model CreateBookRequest {
  @doc("Tên sách")
  @minLength(1)
  @maxLength(255)
  name: string;

  @doc("Tên tác giả")
  @minLength(1)
  @maxLength(255)
  author_name: string;

  @doc("Mô tả sách")
  @minLength(1)
  @maxLength(1000)
  description: string;
}

/**
 * Request để cập nhật sách
 */
model UpdateBookRequest {
  @doc("Tên sách (optional)")
  @minLength(1)
  @maxLength(255)
  name?: string;

  @doc("Tên tác giả (optional)")
  @minLength(1)
  @maxLength(255)
  author_name?: string;

  @doc("Mô tả sách (optional)")
  @maxLength(1000)
  description?: string;
}

/**
 * Response danh sách sách với pagination
 */
model BookListResponse {
  @doc("Danh sách sách")
  data: Book[];

  @doc("Tổng số sách")
  total: int32;

  @doc("Số sách bỏ qua")
  skip: int32;

  @doc("Số sách trả về")
  limit: int32;
}

/**
 * Response thành công khi tạo/cập nhật sách
 */
model BookResponse {
  @doc("Dữ liệu sách")
  data: Book;

  @doc("Thông báo")
  message: string;
}

/**
 * Response xóa sách thành công
 */
model DeleteResponse {
  @doc("Thông báo xóa thành công")
  message: string;
}

/**
 * Response lỗi
 */
model ErrorResponse {
  @doc("Thông báo lỗi")
  error: string;

  @doc("HTTP status code")
  status: int32;

  @doc("Chi tiết lỗi (nếu có)")
  details?: string[];
}

/**
 * Pagination parameters
 */
model PaginationParams {
  @doc("Số sách bỏ qua")
  @query
  @minValue(0)
  skip?: int32 = 0;

  @doc("Số sách trả về")
  @query
  @minValue(1)
  limit?: int32 = 10;

  @doc("Sắp xếp theo trường")
  @query
  sort_by?: "name" | "author_name" | "created_at" = "created_at";
}

/**
 * Books API Interface
 * Quản lý danh sách sách dalam thư viện
 */
@route("/")
interface BooksAPI {
  /**
   * Lấy danh sách tất cả sách
   * @param params Pagination parameters
   * @returns Danh sách sách thành công
   */
  @doc("Lấy danh sách tất cả sách trong thư viện")
  @get
  @route("/books")
  getAllBooks(...PaginationParams): {
    @statusCode statusCode: 200;
    @body body: BookListResponse;
  } | {
    @statusCode statusCode: 500;
    @body body: ErrorResponse;
  };

  /**
   * Tạo sách mới
   * @param request Thông tin sách cần tạo
   * @returns Sách vừa được tạo
   */
  @doc("Tạo cuốn sách mới trong thư viện")
  @post
  @route("/books")
  createBook(@body request: CreateBookRequest): {
    @statusCode statusCode: 201;
    @body body: BookResponse;
  } | {
    @statusCode statusCode: 400;
    @body body: ErrorResponse;
  } | {
    @statusCode statusCode: 500;
    @body body: ErrorResponse;
  };

  /**
   * Lấy thông tin một sách
   * @param id ID của sách
   * @returns Thông tin sách
   */
  @doc("Lấy thông tin chi tiết của một cuốn sách theo ID")
  @get
  @route("/books/{id}")
  getBook(@path id: string): {
    @statusCode statusCode: 200;
    @body body: {
      data: Book;
    };
  } | {
    @statusCode statusCode: 404;
    @body body: ErrorResponse;
  } | {
    @statusCode statusCode: 500;
    @body body: ErrorResponse;
  };

  /**
   * Cập nhật sách
   * @param id ID của sách
   * @param request Thông tin cập nhật
   * @returns Sách sau khi cập nhật
   */
  @doc("Cập nhật thông tin của một cuốn sách theo ID")
  @put
  @route("/books/{id}")
  updateBook(@path id: string, @body request: UpdateBookRequest): {
    @statusCode statusCode: 200;
    @body body: BookResponse;
  } | {
    @statusCode statusCode: 400;
    @body body: ErrorResponse;
  } | {
    @statusCode statusCode: 404;
    @body body: ErrorResponse;
  } | {
    @statusCode statusCode: 500;
    @body body: ErrorResponse;
  };

  /**
   * Xóa sách
   * @param id ID của sách cần xóa
   * @returns Thông báo xóa thành công
   */
  @doc("Xóa một cuốn sách từ thư viện theo ID")
  @delete
  @route("/books/{id}")
  deleteBook(@path id: string): {
    @statusCode statusCode: 200;
    @body body: DeleteResponse;
  } | {
    @statusCode statusCode: 404;
    @body body: ErrorResponse;
  } | {
    @statusCode statusCode: 500;
    @body body: ErrorResponse;
  };
}

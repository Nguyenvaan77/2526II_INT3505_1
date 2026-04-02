from flask import Blueprint, request, jsonify, Flask
from data import books, loans, authors, members, addresses
from pagination import offset_pagination
from services.author_service import AuthorService
from services.book_service import BookService
from services.member_service import MemberService
from services.loan_service import LoanService
from services.address_service import AddressService
from model.response.author_response import author_response, author_detail_response
from model.response.book_response import book_response, book_detail_response
from model.response.member_response import member_response
from model.response.loan_response import loan_response, loan_detail_response
from model.response.address_response import address_response, address_detail_response
from model.request.author_request import CreateAuthorRequest, UpdateAuthorRequest
from model.request.book_request import CreateBookRequest, UpdateBookRequest
from model.request.member_request import CreateMemberRequest, UpdateMemberRequest
from model.request.loan_request import CreateLoanRequest, UpdateLoanRequest
from model.request.address_request import CreateAddressRequest, UpdateAddressRequest

v1 = Blueprint("v1", __name__, url_prefix="/api/v1")


# ==================== AUTHOR APIs ====================

@v1.route("/authors", methods=["GET"])
def get_authors():
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 5))
    
    authors_list = AuthorService.get_all_authors()
    result = offset_pagination(authors_list, offset, limit)
    
    # Áp dụng response transformation
    result["data"] = [author_response(a) for a in result["data"]]
    
    return jsonify(result)


@v1.route("/authors/<int:author_id>", methods=["GET"])
def get_author(author_id):
    author = AuthorService.get_author_by_id(author_id)
    
    if author is None:
        return jsonify({"error": "Author not found"}), 404
    
    return jsonify(author_response(author))


@v1.route("/authors", methods=["POST"])
def create_author():
    data = request.get_json()
    
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' field"}), 400
    
    author_request = CreateAuthorRequest(name=data["name"])
    new_author = AuthorService.create_author(author_request)
    
    return jsonify(author_response(new_author)), 201


@v1.route("/authors/<int:author_id>", methods=["PUT"])
def update_author(author_id):
    data = request.get_json()
    
    author_request = UpdateAuthorRequest(name=data.get("name"))
    updated_author = AuthorService.update_author(author_id, author_request)
    
    if updated_author is None:
        return jsonify({"error": "Author not found"}), 404
    
    return jsonify(author_response(updated_author))


@v1.route("/authors/<int:author_id>", methods=["DELETE"])
def delete_author(author_id):
    success = AuthorService.delete_author(author_id)
    
    if not success:
        return jsonify({"error": "Author not found"}), 404
    
    return jsonify({"message": "Author deleted successfully"}), 200


# ==================== BOOK APIs ====================

@v1.route("/books", methods=["GET"])
def get_books():
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 5))
    
    books_list = BookService.get_all_books()
    result = offset_pagination(books_list, offset, limit)
    
    # Áp dụng response transformation
    result["data"] = [book_response(b) for b in result["data"]]
    
    return jsonify(result)


@v1.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = BookService.get_book_by_id(book_id)
    
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    
    return jsonify(book_response(book))


@v1.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()
    
    if not data or "title" not in data or "author_id" not in data or "year" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    book_request = CreateBookRequest(
        title=data["title"],
        author_id=data["author_id"],
        year=data["year"]
    )
    new_book = BookService.create_book(book_request)
    
    return jsonify(book_response(new_book)), 201


@v1.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json()
    
    book_request = UpdateBookRequest(
        title=data.get("title"),
        author_id=data.get("author_id"),
        year=data.get("year")
    )
    updated_book = BookService.update_book(book_id, book_request)
    
    if updated_book is None:
        return jsonify({"error": "Book not found"}), 404
    
    return jsonify(book_response(updated_book))


@v1.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    success = BookService.delete_book(book_id)
    
    if not success:
        return jsonify({"error": "Book not found"}), 404
    
    return jsonify({"message": "Book deleted successfully"}), 200


# ==================== MEMBER APIs ====================

@v1.route("/members", methods=["GET"])
def get_members():
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 5))
    
    members_list = MemberService.get_all_members()
    result = offset_pagination(members_list, offset, limit)
    
    # Áp dụng response transformation
    result["data"] = [member_response(m) for m in result["data"]]
    
    return jsonify(result)


@v1.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    member = MemberService.get_member_by_id(member_id)
    
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    
    return jsonify(member_response(member))


@v1.route("/members", methods=["POST"])
def create_member():
    data = request.get_json()
    
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' field"}), 400
    
    member_request = CreateMemberRequest(name=data["name"])
    new_member = MemberService.create_member(member_request)
    
    return jsonify(member_response(new_member)), 201


@v1.route("/members/<int:member_id>", methods=["PUT"])
def update_member(member_id):
    data = request.get_json()
    
    member_request = UpdateMemberRequest(name=data.get("name"))
    updated_member = MemberService.update_member(member_id, member_request)
    
    if updated_member is None:
        return jsonify({"error": "Member not found"}), 404
    
    return jsonify(member_response(updated_member))


@v1.route("/members/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    success = MemberService.delete_member(member_id)
    
    if not success:
        return jsonify({"error": "Member not found"}), 404
    
    return jsonify({"message": "Member deleted successfully"}), 200


# ==================== LOAN APIs ====================

@v1.route("/loans", methods=["GET"])
def get_loans():
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 5))
    
    loans_list = LoanService.get_all_loans()
    result = offset_pagination(loans_list, offset, limit)
    
    # Áp dụng response transformation
    result["data"] = [loan_response(l) for l in result["data"]]
    
    return jsonify(result)


@v1.route("/loans/<int:loan_id>", methods=["GET"])
def get_loan(loan_id):
    loan = LoanService.get_loan_by_id(loan_id)
    
    if loan is None:
        return jsonify({"error": "Loan not found"}), 404
    
    return jsonify(loan_response(loan))


@v1.route("/loans", methods=["POST"])
def create_loan():
    data = request.get_json()
    
    if not data or "book_id" not in data or "member_id" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    loan_request = CreateLoanRequest(
        book_id=data["book_id"],
        member_id=data["member_id"]
    )
    new_loan = LoanService.create_loan(loan_request)
    
    if new_loan is None:
        return jsonify({"error": "Invalid book_id or member_id"}), 400
    
    return jsonify(loan_response(new_loan)), 201


@v1.route("/loans/<int:loan_id>", methods=["PUT"])
def update_loan(loan_id):
    data = request.get_json()
    
    loan_request = UpdateLoanRequest(
        book_id=data.get("book_id"),
        member_id=data.get("member_id")
    )
    updated_loan = LoanService.update_loan(loan_id, loan_request)
    
    if updated_loan is None:
        return jsonify({"error": "Loan not found"}), 404
    
    return jsonify(loan_response(updated_loan))


@v1.route("/loans/<int:loan_id>", methods=["DELETE"])
def delete_loan(loan_id):
    success = LoanService.delete_loan(loan_id)
    
    if not success:
        return jsonify({"error": "Loan not found"}), 404
    
    return jsonify({"message": "Loan deleted successfully"}), 200


# ==================== ADDRESS APIs ====================

@v1.route("/addresses", methods=["GET"])
def get_addresses():
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 5))
    author_id = request.args.get("author_id")
    
    if author_id:
        addresses_list = AddressService.get_addresses_by_author(int(author_id))
    else:
        addresses_list = AddressService.get_all_addresses()
    
    result = offset_pagination(addresses_list, offset, limit)
    
    # Áp dụng response transformation
    result["data"] = [address_response(a) for a in result["data"]]
    
    return jsonify(result)


@v1.route("/addresses/<int:address_id>", methods=["GET"])
def get_address(address_id):
    address = AddressService.get_address_by_id(address_id)
    
    if address is None:
        return jsonify({"error": "Address not found"}), 404
    
    return jsonify(address_response(address))


@v1.route("/authors/<int:author_id>/addresses", methods=["GET"])
def get_author_addresses(author_id):
    author = AuthorService.get_author_by_id(author_id)
    if author is None:
        return jsonify({"error": "Author not found"}), 404
    
    author_addresses = AddressService.get_addresses_by_author(author_id)
    return jsonify([address_response(a) for a in author_addresses])


@v1.route("/authors/<int:author_id>/addresses/<int:address_id>", methods=["GET"])
def get_author_address(author_id, address_id):
    address = AddressService.get_address_by_id(address_id)
    
    if address is None or address["author_id"] != author_id:
        return jsonify({"error": "Address not found"}), 404
    
    return jsonify(address_response(address))


@v1.route("/addresses", methods=["POST"])
def create_address():
    data = request.get_json()
    
    if not data or "author_id" not in data or "city" not in data or "country" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    address_request = CreateAddressRequest(
        author_id=data["author_id"],
        city=data["city"],
        country=data["country"]
    )
    new_address = AddressService.create_address(address_request)
    
    if new_address is None:
        return jsonify({"error": "Invalid author_id"}), 400
    
    return jsonify(address_response(new_address)), 201


@v1.route("/addresses/<int:address_id>", methods=["PUT"])
def update_address(address_id):
    data = request.get_json()
    
    address_request = UpdateAddressRequest(
        city=data.get("city"),
        country=data.get("country")
    )
    updated_address = AddressService.update_address(address_id, address_request)
    
    if updated_address is None:
        return jsonify({"error": "Address not found"}), 404
    
    return jsonify(address_response(updated_address))


@v1.route("/addresses/<int:address_id>", methods=["DELETE"])
def delete_address(address_id):
    success = AddressService.delete_address(address_id)
    
    if not success:
        return jsonify({"error": "Address not found"}), 404
    
    return jsonify({"message": "Address deleted successfully"}), 200


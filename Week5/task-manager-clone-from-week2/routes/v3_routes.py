from flask import Blueprint, request, jsonify
from data import authors, books, members, loans
from pagination import cursor_pagination
from services.author_service import AuthorService
from services.book_service import BookService
from services.member_service import MemberService
from services.loan_service import LoanService
from model.response.author_response import author_response
from model.response.book_response import book_response
from model.response.member_response import member_response
from model.response.loan_response import loan_response

v3 = Blueprint("v3", __name__, url_prefix="/api/v3")


# ==================== AUTHOR APIs ====================

@v3.route("/authors", methods=["GET"])
def get_authors():
    cursor = request.args.get("cursor")
    limit = int(request.args.get("limit", 5))
    
    if cursor:
        cursor = int(cursor)
    
    authors_list = AuthorService.get_all_authors()
    result = cursor_pagination(authors_list, cursor, limit)
    
    # Áp dụng response transformation
    result["data"] = [author_response(a) for a in result["data"]]
    
    return jsonify(result)


# ==================== BOOK APIs ====================

@v3.route("/books", methods=["GET"])
def get_books():
    cursor = request.args.get("cursor")
    limit = int(request.args.get("limit", 5))
    
    if cursor:
        cursor = int(cursor)
    
    books_list = BookService.get_all_books()
    result = cursor_pagination(books_list, cursor, limit)
    
    # Áp dụng response transformation
    result["data"] = [book_response(b) for b in result["data"]]
    
    return jsonify(result)


# ==================== MEMBER APIs ====================

@v3.route("/members", methods=["GET"])
def get_members():
    cursor = request.args.get("cursor")
    limit = int(request.args.get("limit", 5))
    
    if cursor:
        cursor = int(cursor)
    
    members_list = MemberService.get_all_members()
    result = cursor_pagination(members_list, cursor, limit)
    
    # Áp dụng response transformation
    result["data"] = [member_response(m) for m in result["data"]]
    
    return jsonify(result)


# ==================== LOAN APIs ====================

@v3.route("/loans", methods=["GET"])
def get_loans():
    cursor = request.args.get("cursor")
    limit = int(request.args.get("limit", 5))
    
    if cursor:
        cursor = int(cursor)
    
    loans_list = LoanService.get_all_loans()
    result = cursor_pagination(loans_list, cursor, limit)
    
    # Áp dụng response transformation
    result["data"] = [loan_response(l) for l in result["data"]]
    
    return jsonify(result)

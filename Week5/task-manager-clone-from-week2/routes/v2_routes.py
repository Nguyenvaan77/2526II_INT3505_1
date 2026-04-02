from flask import Blueprint, request, jsonify
from data import authors, books, members, loans
from pagination import page_pagination
from services.author_service import AuthorService
from services.book_service import BookService
from services.member_service import MemberService
from services.loan_service import LoanService
from model.response.author_response import author_response
from model.response.book_response import book_response
from model.response.member_response import member_response
from model.response.loan_response import loan_response

v2 = Blueprint("v2", __name__, url_prefix="/api/v2")


# ==================== AUTHOR APIs ====================

@v2.route("/authors", methods=["GET"])
def get_authors():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 5))
    
    authors_list = AuthorService.get_all_authors()
    result = page_pagination(authors_list, page, size)
    
    # Áp dụng response transformation
    result["data"] = [author_response(a) for a in result["data"]]
    
    return jsonify(result)


# ==================== BOOK APIs ====================

@v2.route("/books", methods=["GET"])
def get_books():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 5))
    
    books_list = BookService.get_all_books()
    result = page_pagination(books_list, page, size)
    
    # Áp dụng response transformation
    result["data"] = [book_response(b) for b in result["data"]]
    
    return jsonify(result)


# ==================== MEMBER APIs ====================

@v2.route("/members", methods=["GET"])
def get_members():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 5))
    
    members_list = MemberService.get_all_members()
    result = page_pagination(members_list, page, size)
    
    # Áp dụng response transformation
    result["data"] = [member_response(m) for m in result["data"]]
    
    return jsonify(result)


# ==================== LOAN APIs ====================

@v2.route("/loans", methods=["GET"])
def get_loans():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 5))
    
    loans_list = LoanService.get_all_loans()
    result = page_pagination(loans_list, page, size)
    
    # Áp dụng response transformation
    result["data"] = [loan_response(l) for l in result["data"]]
    
    return jsonify(result)

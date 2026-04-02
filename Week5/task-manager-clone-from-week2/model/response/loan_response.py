def loan_response(loan):
    return {
        "id": loan["id"],
        "book_id": loan["book_id"],
        "member_id": loan["member_id"]
    }


def loan_detail_response(loan, book=None, member=None):
    """Response với thông tin chi tiết sách và thành viên liên quan"""
    response = {
        "id": loan["id"],
        "book_id": loan["book_id"],
        "member_id": loan["member_id"]
    }
    
    if book:
        response["book"] = {
            "id": book["id"],
            "title": book["title"],
            "author_id": book["author_id"],
            "year": book["year"]
        }
    
    if member:
        response["member"] = {
            "id": member["id"],
            "name": member["name"]
        }
    
    return response

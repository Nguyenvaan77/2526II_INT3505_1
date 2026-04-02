def book_response(book):
    return {
        "id": book["id"],
        "title": book["title"],
        "author_id": book["author_id"],
        "year": book["year"]
    }


def book_detail_response(book, author=None):
    """Response với thông tin chi tiết tác giả"""
    response = {
        "id": book["id"],
        "title": book["title"],
        "author_id": book["author_id"],
        "year": book["year"]
    }
    
    if author:
        response["author"] = {
            "id": author["id"],
            "name": author["name"]
        }
    
    return response
def address_response(address):
    return {
        "id": address["id"],
        "author_id": address["author_id"],
        "city": address["city"],
        "country": address["country"]
    }


def address_detail_response(address, author=None):
    """Response với thông tin chi tiết tác giả liên quan"""
    response = {
        "id": address["id"],
        "author_id": address["author_id"],
        "city": address["city"],
        "country": address["country"]
    }
    
    if author:
        response["author"] = {
            "id": author["id"],
            "name": author["name"]
        }
    
    return response

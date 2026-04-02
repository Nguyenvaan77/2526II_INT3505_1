def author_response(author):
    return {
        "id": author["id"],
        "name": author["name"]
    }


def author_detail_response(author, addresses=None):
    """Response với danh sách địa chỉ của tác giả"""
    response = {
        "id": author["id"],
        "name": author["name"]
    }
    
    if addresses:
        response["addresses"] = [
            {
                "id": addr["id"],
                "city": addr["city"],
                "country": addr["country"]
            }
            for addr in addresses
        ]
    
    return response
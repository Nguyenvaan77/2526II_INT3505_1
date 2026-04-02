from data import authors, addresses


class AuthorService:
    """Service xử lý logic liên quan đến Author"""
    
    @staticmethod
    def get_all_authors():
        """Lấy tất cả tác giả"""
        return authors
    
    @staticmethod
    def get_author_by_id(author_id):
        """Lấy tác giả theo ID"""
        author = next((a for a in authors if a["id"] == author_id), None)
        return author
    
    @staticmethod
    def get_author_with_addresses(author_id):
        """Lấy tác giả và danh sách địa chỉ"""
        author = AuthorService.get_author_by_id(author_id)
        if not author:
            return None
        
        author_addresses = [a for a in addresses if a["author_id"] == author_id]
        return {
            "author": author,
            "addresses": author_addresses
        }
    
    @staticmethod
    def create_author(request):
        """Tạo tác giả mới"""
        new_id = max([a["id"] for a in authors], default=0) + 1
        new_author = {
            "id": new_id,
            "name": request.name
        }
        authors.append(new_author)
        return new_author
    
    @staticmethod
    def update_author(author_id, request):
        """Cập nhật thông tin tác giả"""
        author = AuthorService.get_author_by_id(author_id)
        if not author:
            return None
        
        if request.name is not None:
            author["name"] = request.name
        
        return author
    
    @staticmethod
    def delete_author(author_id):
        """Xóa tác giả"""
        global authors
        author = AuthorService.get_author_by_id(author_id)
        if not author:
            return False
        
        authors = [a for a in authors if a["id"] != author_id]
        return True

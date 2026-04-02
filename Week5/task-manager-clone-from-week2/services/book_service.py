from data import books, authors


class BookService:
    """Service xử lý logic liên quan đến Book"""
    
    @staticmethod
    def get_all_books():
        """Lấy tất cả sách"""
        return books
    
    @staticmethod
    def get_book_by_id(book_id):
        """Lấy sách theo ID"""
        book = next((b for b in books if b["id"] == book_id), None)
        return book
    
    @staticmethod
    def get_book_with_author(book_id):
        """Lấy sách và thông tin tác giả"""
        book = BookService.get_book_by_id(book_id)
        if not book:
            return None
        
        author = next((a for a in authors if a["id"] == book["author_id"]), None)
        return {
            "book": book,
            "author": author
        }
    
    @staticmethod
    def get_books_by_author(author_id):
        """Lấy tất cả sách của một tác giả"""
        return [b for b in books if b["author_id"] == author_id]
    
    @staticmethod
    def create_book(request):
        """Tạo sách mới"""
        new_id = max([b["id"] for b in books], default=0) + 1
        new_book = {
            "id": new_id,
            "title": request.title,
            "author_id": request.author_id,
            "year": request.year
        }
        books.append(new_book)
        return new_book
    
    @staticmethod
    def update_book(book_id, request):
        """Cập nhật thông tin sách"""
        book = BookService.get_book_by_id(book_id)
        if not book:
            return None
        
        if request.title is not None:
            book["title"] = request.title
        if request.author_id is not None:
            book["author_id"] = request.author_id
        if request.year is not None:
            book["year"] = request.year
        
        return book
    
    @staticmethod
    def delete_book(book_id):
        """Xóa sách"""
        global books
        book = BookService.get_book_by_id(book_id)
        if not book:
            return False
        
        books = [b for b in books if b["id"] != book_id]
        return True

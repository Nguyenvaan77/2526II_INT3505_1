from data import loans, books, members


class LoanService:
    """Service xử lý logic liên quan đến Loan"""
    
    @staticmethod
    def get_all_loans():
        """Lấy tất cả khoản mượn"""
        return loans
    
    @staticmethod
    def get_loan_by_id(loan_id):
        """Lấy khoản mượn theo ID"""
        loan = next((l for l in loans if l["id"] == loan_id), None)
        return loan
    
    @staticmethod
    def get_loan_with_details(loan_id):
        """Lấy khoản mượn và thông tin sách, thành viên"""
        loan = LoanService.get_loan_by_id(loan_id)
        if not loan:
            return None
        
        book = next((b for b in books if b["id"] == loan["book_id"]), None)
        member = next((m for m in members if m["id"] == loan["member_id"]), None)
        
        return {
            "loan": loan,
            "book": book,
            "member": member
        }
    
    @staticmethod
    def get_loans_by_member(member_id):
        """Lấy tất cả khoản mượn của một thành viên"""
        return [l for l in loans if l["member_id"] == member_id]
    
    @staticmethod
    def get_loans_by_book(book_id):
        """Lấy tất cả khoản mượn của một sách"""
        return [l for l in loans if l["book_id"] == book_id]
    
    @staticmethod
    def create_loan(request):
        """Tạo khoản mượn mới"""
        # Kiểm tra xem sách và thành viên có tồn tại không
        book = next((b for b in books if b["id"] == request.book_id), None)
        member = next((m for m in members if m["id"] == request.member_id), None)
        
        if not book or not member:
            return None
        
        new_id = max([l["id"] for l in loans], default=0) + 1
        new_loan = {
            "id": new_id,
            "book_id": request.book_id,
            "member_id": request.member_id
        }
        loans.append(new_loan)
        return new_loan
    
    @staticmethod
    def update_loan(loan_id, request):
        """Cập nhật thông tin khoản mượn"""
        loan = LoanService.get_loan_by_id(loan_id)
        if not loan:
            return None
        
        if request.book_id is not None:
            book = next((b for b in books if b["id"] == request.book_id), None)
            if book:
                loan["book_id"] = request.book_id
        
        if request.member_id is not None:
            member = next((m for m in members if m["id"] == request.member_id), None)
            if member:
                loan["member_id"] = request.member_id
        
        return loan
    
    @staticmethod
    def delete_loan(loan_id):
        """Xóa khoản mượn"""
        global loans
        loan = LoanService.get_loan_by_id(loan_id)
        if not loan:
            return False
        
        loans = [l for l in loans if l["id"] != loan_id]
        return True

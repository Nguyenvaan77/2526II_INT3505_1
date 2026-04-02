class CreateLoanRequest:
    def __init__(self, book_id, member_id):
        self.book_id = book_id
        self.member_id = member_id


class UpdateLoanRequest:
    def __init__(self, book_id=None, member_id=None):
        self.book_id = book_id
        self.member_id = member_id

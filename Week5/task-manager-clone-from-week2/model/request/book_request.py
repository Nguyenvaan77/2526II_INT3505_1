class CreateBookRequest:
    def __init__(self, title, author_id, year):
        self.title = title
        self.author_id = author_id
        self.year = year


class UpdateBookRequest:
    def __init__(self, title=None, author_id=None, year=None):
        self.title = title
        self.author_id = author_id
        self.year = year
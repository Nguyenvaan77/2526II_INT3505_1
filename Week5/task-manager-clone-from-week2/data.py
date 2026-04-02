authors = [
    {"id": 1, "name": "George Orwell"},
    {"id": 2, "name": "J.K Rowling"},
]

addresses = [
    {"id": 1, "author_id": 1, "city": "London", "country": "UK"},
    {"id": 2, "author_id": 1, "city": "Paris", "country": "France"},
    {"id": 3, "author_id": 2, "city": "Edinburgh", "country": "UK"}
]

books = [
    {"id": 1, "title": "1984", "author_id": 1, "year": 1949},
    {"id": 2, "title": "Animal Farm", "author_id": 1, "year": 1945},
    {"id": 3, "title": "Harry Potter 1", "author_id": 2, "year": 1997},
    {"id": 4, "title": "Harry Potter 2", "author_id": 2, "year": 1998},
    {"id": 5, "title": "Harry Potter 3", "author_id": 2, "year": 1999},
    {"id": 6, "title": "Harry Potter 4", "author_id": 2, "year": 2000},
    {"id": 7, "title": "Harry Potter 5", "author_id": 2, "year": 2003},
]

members = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Van B"},
]

loans = [
    {"id": 1, "book_id": 1, "member_id": 1},
    {"id": 2, "book_id": 2, "member_id": 2},
]
class CreateAddressRequest:
    def __init__(self, author_id, city, country):
        self.author_id = author_id
        self.city = city
        self.country = country


class UpdateAddressRequest:
    def __init__(self, city=None, country=None):
        self.city = city
        self.country = country

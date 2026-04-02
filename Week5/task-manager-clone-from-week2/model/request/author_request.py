class CreateAuthorRequest:
    def __init__(self, name):
        self.name = name


class UpdateAuthorRequest:
    def __init__(self, name=None):
        self.name = name
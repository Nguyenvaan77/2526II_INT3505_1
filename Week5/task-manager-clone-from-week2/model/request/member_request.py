class CreateMemberRequest:
    def __init__(self, name):
        self.name = name


class UpdateMemberRequest:
    def __init__(self, name=None):
        self.name = name

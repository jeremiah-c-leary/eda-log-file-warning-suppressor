


class create():

    def __init__(self, warning_id=None, message=None, author=None):
        self.warning_id = warning_id
        self.message = message
        self.author = author

    def get_warning_id(self):
        return self.warning_id

    def get_message(self):
        return self.message

    def get_author(self):
        return self.author

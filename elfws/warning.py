

class create():

    def __init__(self, warning_id=None, message=None, filename=None, linenumber=None):
        self.warning_id = warning_id
        self.message = message
        self.filename = filename
        self.linenumber = linenumber

    def get_warning_id(self):
        return self.warning_id

    def get_message(self):
        return self.message

    def get_filename(self):
        return self.filename

    def get_linenumber(self):
        return self.linenumber

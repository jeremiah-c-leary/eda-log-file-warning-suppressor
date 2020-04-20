

class create():

    def __init__(self, warning_id=None, message=None, filename=None, linenumber=None):
        self.warning_id = warning_id
        self.message = message
        self.filename = filename
        self.linenumber = linenumber
        self.suppressed_by = []

    def add_suppression_rule(self, oRule):
        self.suppressed_by.append(oRule)

    def get_id(self):
        return self.warning_id

    def get_filename(self):
        return self.filename

    def get_suppressed_by_rules(self):
        return self.suppressed_by

    def get_linenumber(self):
        return self.linenumber

    def get_message(self):
        return self.message

    def is_suppressed(self):
        if len(self.suppressed_by) == 0:
            return False
        return True

    def is_suppressed_by_multiple_rules(self):
        if len(self.suppressed_by) > 1:
            return True
        return False

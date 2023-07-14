

class create():

    def __init__(self, warning_id=None, message=None, author=None, comment=None):
        self.warning_id = warning_id
        self.message = message
        self.author = author
        self.comment = comment
        self.investigate = False
        self.suppressed_warnings = []
        self.options = []

    def add_suppressed_warning(self, oWarning):
        self.suppressed_warnings.append(oWarning)

    def get_author(self):
        return self.author

    def get_comment(self):
        return self.comment

    def get_investigate(self):
        return self.investigate

    def get_message(self):
        return self.message

    def get_suppressed_warnings(self):
        return self.suppressed_warnings

    def get_warning_id(self):
        return self.warning_id

    def has_suppressed_a_warning(self):
        if len(self.suppressed_warnings) == 0:
            return False
        return True

    def is_investigation_rule(self):
        return self.investigate

    def has_option(self, sOption):
        if sOption in self.options:
            return True
        return False

    def set_options(self, lOptions):
        self.options = lOptions

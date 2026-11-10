
from elfws import deprecation


class LogWarning():

    def __init__(self, warning_id=None, message=None, filename=None, linenumber=None):
        self.warning_id = warning_id
        self.message = message
        self.filename = filename
        self.linenumber = linenumber
        self.investigate = False
        self.suppressed_by = []

    def add_suppression_rule(self, oRule):
        self.suppressed_by.append(oRule)

    def get_id(self):
        return self.warning_id

    def get_investigate(self):
        return self.investigate

    def get_filename(self):
        return self.filename

    def get_suppressed_by_rules(self):
        return self.suppressed_by

    def get_linenumber(self):
        return self.linenumber

    def get_message(self):
        return self.message

    def is_investigate(self):
        return self.investigate

    def is_suppressed(self):
        return len(self.suppressed_by) > 0

    def is_suppressed_by_multiple_rules(self):
        return len(self.suppressed_by) > 1

    def set_investigate(self):
        self.investigate = True


__getattr__ = deprecation.build_module_getattr(__name__, {'create': LogWarning})

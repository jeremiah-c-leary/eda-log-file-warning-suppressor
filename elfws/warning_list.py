

class create():

    def __init__(self):
        self.warnings = []

    def add_warning(self, oWarning):
        self.warnings.append(oWarning)

    def has_warnings(self):
        if len(self.warnings) == 0:
            return False
        return True

    def get_number_of_warnings(self):
        return len(self.warnings)
    
    def get_warnings(self):
        return self.warnings

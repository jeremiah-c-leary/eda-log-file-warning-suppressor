

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

    def get_warnings_suppressed_by_multiple_rules(self):
        lReturn = []
        for oWarning in self.warnings:
            if oWarning.is_suppressed_by_multiple_rules():
                lReturn.append(oWarning)
        return lReturn

    def get_suppressed_warnings(self):
        lReturn = []
        for oWarning in self.warnings:
            if oWarning.is_suppressed() and not oWarning.is_investigate():
                lReturn.append(oWarning)
        return lReturn

    def get_unsuppressed_warnings(self):
        lReturn = []
        for oWarning in self.warnings:
            if not oWarning.is_suppressed():
                lReturn.append(oWarning)
        return lReturn

    def get_maximum_id_length(self):
        iReturn = 0
        for oWarning in self.warnings:
            iReturn = max(iReturn, len(oWarning.get_id()))
        return iReturn

    def get_investigate_warnings(self):
        lReturn = []
        for oWarning in self.warnings:
            if oWarning.is_suppressed() and oWarning.is_investigate():
                lReturn.append(oWarning)
        return lReturn

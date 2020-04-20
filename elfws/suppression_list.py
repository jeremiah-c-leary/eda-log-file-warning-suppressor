

class create():

    def __init__(self):
        self.suppressions = []

    def add_suppression(self, oSuppression):
        self.suppressions.append(oSuppression)

    def get_number_of_suppressions(self):
        return len(self.suppressions)

    def get_suppressions(self):
        return self.suppressions

    def get_suppressions_which_suppressed_a_warning(self):
        lReturn = []
        for oSup in self.suppressions:
            if oSup.has_suppressed_a_warning():
                lReturn.append(oSup)
        return lReturn

    def get_suppressions_which_did_not_suppress_a_warning(self):
        lReturn = []
        for oSup in self.suppressions:
            if not oSup.has_suppressed_a_warning():
                lReturn.append(oSup)
        return lReturn

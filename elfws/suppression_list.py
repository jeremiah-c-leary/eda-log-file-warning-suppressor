

class create():

    def __init__(self):
        self.suppressions = []

    def add_suppression(self, oSuppression):
        self.suppressions.append(oSuppression)

    def get_number_of_suppressions(self):
        return len(self.suppressions)

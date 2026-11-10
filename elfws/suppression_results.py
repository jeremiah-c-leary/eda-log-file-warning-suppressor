
from elfws import log_file
from elfws import rule_matching
from elfws import suppression_file
from elfws import suppression_list


def apply_suppression_file(sLogFileName, sSuppressionFileName):
    oSupList = suppression_file.read_suppression_list(sSuppressionFileName)
    oWarnList = log_file.read_warning_list(sLogFileName)
    oResults = SuppressionResults(sLogFileName, oWarnList, sSuppressionFileName, oSupList)
    oResults.apply_suppression_rules()
    return oResults


def create_results_without_suppression_file(sLogFileName):
    oWarnList = log_file.read_warning_list(sLogFileName)
    oSupList = suppression_list.SuppressionList()
    return SuppressionResults(sLogFileName, oWarnList, suppression_file.NOT_SPECIFIED, oSupList)


class SuppressionResults():
    '''
    The warnings in a log file after a suppression file has been applied to them.
    '''

    def __init__(self, sLogFileName, oWarnList, sSuppressionFileName, oSupList):
        self.sLogFileName = sLogFileName
        self.oWarnList = oWarnList
        self.sSuppressionFileName = sSuppressionFileName
        self.oSupList = oSupList

    def apply_suppression_rules(self):
        for oWarning in self.oWarnList.get_warnings():
            for oSuppression in self.oSupList.get_suppressions():
                rule_matching.suppress_warning_with_rule(oWarning, oSuppression)

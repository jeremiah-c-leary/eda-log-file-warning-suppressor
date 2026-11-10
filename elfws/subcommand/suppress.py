
import sys

from elfws import warning_list
from elfws import log_file
from elfws import rule_matching
from elfws import suppression_file
from elfws import display
from elfws.exit_code import ExitCode


def suppress(oCommandLineArguments):

    oSupList = suppression_file.read_suppression_list(oCommandLineArguments.suppression_file)
    oWarnList = log_file.read_warning_list(oCommandLineArguments.log_file)
    rule_matching.apply_suppression_rules_to_warnings(oWarnList, oSupList)

    display.results(oCommandLineArguments.log_file, oCommandLineArguments.suppression_file, oSupList, oWarnList)

    sys.exit(ExitCode.SUCCESS)


def extract_non_suppressed_warnings(oWarnList, oSupList):
    oReturn = warning_list.WarningList()
    for oWarning in oWarnList.get_warnings():
        fMatchFound = False
        for oSuppression in oSupList.get_suppressions():
            fMatchFound = rule_matching.check_for_match(oWarning, oSuppression)
            if fMatchFound:
                break
        if not fMatchFound:
            oReturn.add_warning(oWarning)

    return oReturn


import re
import sys

from elfws import warning_list
from elfws import utils
from elfws import display


def suppress(cla):

    dSup = utils.read_suppression_file(cla.suppression_file)
    oSupList = utils.create_suppression_list(dSup)

    lLogFile = utils.read_log_file(cla.log_file)

    oWarnList = utils.create_warning_list(lLogFile, cla.log_file)

    utils.apply_suppression_rules_to_warnings(oWarnList, oSupList)
    oNonSuppressedWarnings = oWarnList.get_unsuppressed_warnings()

    display.results(cla.log_file, cla.suppression_file, oSupList, oWarnList)


def extract_non_suppressed_warnings(oWarnList, oSupList):
    oReturn = warning_list.create()
    for oWarning in oWarnList.get_warnings():
        fMatchFound = False
        for oSuppression in oSupList.get_suppressions():
            fMatchFound = utils.check_for_match(oWarning, oSuppression)
            if fMatchFound:
                break
        if not fMatchFound:
            oReturn.add_warning(oWarning)

    return oReturn

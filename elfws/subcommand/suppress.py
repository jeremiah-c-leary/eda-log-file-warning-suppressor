
import re
import sys

from elfws import warning_list
from elfws import utils


def suppress(cla):

    dSup = utils.read_suppression_file(cla.suppression_file)
    oSupList = utils.create_suppression_list(dSup)

    lLogFile = utils.read_log_file(cla.log_file)

    try:
        mTool = utils.get_vendor_tool_module(lLogFile)
        oWarnList = mTool.extract_warnings(lLogFile)
    except AttributeError:
        print('ERROR: Log file ' + cla.log_file + ' is not supported.')
        sys.exit(1)

    oNonSuppressWarnings = extract_non_suppressed_warnings(oWarnList, oSupList)
    for oWarning in oNonSuppressWarnings.get_warnings():
        print(oWarning.get_id() + '  [' + str(oWarning.get_linenumber()) + '] ' + oWarning.get_message())

def extract_non_suppressed_warnings(oWarnList, oSupList):
    oReturn = warning_list.create()
    for oWarning in oWarnList.get_warnings():
        fMatchFound = False
        for oSuppression in oSupList.get_suppressions():
            if oWarning.get_id() == oSuppression.get_warning_id():
                if re.match('^.*' + oSuppression.get_message(), oWarning.get_message()):
                    fMatchFound = True
                    break
        if not fMatchFound:
            oReturn.add_warning(oWarning)

    return oReturn

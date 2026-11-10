
from elfws import warning
from elfws import warning_list
from elfws.vendor import utils as vendor_utils

LAST_HEADER_LINE_INDEX = 5


def get_vendor():
    return ['Synopsys']


def get_tool_name():
    return 'Synplify Pro'


def is_logfile(lFile):
    for iLineNumber, sLine in enumerate(lFile):
        if sLine.startswith('#Build: Synplify Pro (R)'):
            return True
        if iLineNumber == LAST_HEADER_LINE_INDEX:
            return False
    return False


def extract_warnings(lFile):
    oReturn = warning_list.WarningList()

    for iLineNumber, sLine in enumerate(lFile):
        if sLine.startswith('@W'):
            sID, sMessage = vendor_utils.split_id_and_message(sLine)
            oWarning = warning.LogWarning(sID, sMessage, None, iLineNumber + 1)
            oReturn.add_warning(oWarning)
    return oReturn

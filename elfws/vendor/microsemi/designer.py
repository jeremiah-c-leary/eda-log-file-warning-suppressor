
from elfws import warning
from elfws import warning_list
from elfws.vendor import utils as vendor_utils

LAST_HEADER_LINE_INDEX = 10


def get_vendor():
    return ['Actel', 'Microsemi']


def get_tool_name():
    return 'designer'


def is_logfile(lFile):
    for iLineNumber, sLine in enumerate(lFile):
        if sLine.startswith('Microsemi Libero Software'):
            return True
        if iLineNumber == LAST_HEADER_LINE_INDEX:
            return False
    return False


def extract_warnings(lFile):
    oReturn = warning_list.WarningList()

    fWarningFound = False
    for iLineNumber, sLine in enumerate(lFile):
        # Clear the warning found flag
        if not sLine.startswith(' ') and fWarningFound:
            fWarningFound = False
            oReturn.add_warning(oWarning)
        if sLine.startswith(' ') and fWarningFound:
            oWarning.message += ' ' + sLine.strip()
        if sLine.startswith('Warning:'):
            fWarningFound = True
            sID, sMessage = extract_id_and_message(sLine)
            oWarning = warning.LogWarning(sID, sMessage, None, iLineNumber + 1)

    if fWarningFound:
        oReturn.add_warning(oWarning)

    return oReturn


def extract_id_and_message(sLine):
    sId, sMessage = vendor_utils.split_id_and_message(sLine)
    return vendor_utils.reject_ids_containing_spaces(sLine, sId, sMessage)

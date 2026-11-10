
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
            sID, sMessage = extract_id_and_message(sLine)
            oWarning = warning.LogWarning(sID, sMessage, None, iLineNumber + 1)
            oReturn.add_warning(oWarning)
    return oReturn


def extract_id_and_message(sLine):
    sText = text_after_keyword(sLine)
    if not has_id_separator(sText):
        return vendor_utils.NO_ID, sText.strip()

    sId, sMessage = sText.split(':', 1)
    return sId.strip(), sMessage.strip()


def text_after_keyword(sLine):
    return sLine.split(':', 1)[1]


def has_id_separator(sText):
    return ':' in sText

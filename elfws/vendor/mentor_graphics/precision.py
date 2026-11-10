
from elfws import warning
from elfws import warning_list
from elfws.vendor import utils as vendor_utils

LAST_HEADER_LINE_INDEX = 10


def get_vendor():
    return ['Mentor Graphics']


def get_tool_name():
    return 'precision'


def is_logfile(lFile):
    for iLineNumber, sLine in enumerate(lFile):
        if sLine.startswith('//  Precision RTL Synthesis'):
            return True
        if sLine.startswith('//  Precision Hi-Rel'):
            return True
        if iLineNumber == LAST_HEADER_LINE_INDEX:
            return False
    return False


def extract_warnings(lFile):
    oReturn = warning_list.WarningList()

    for iLineNumber, sLine in enumerate(lFile):
        if sLine.startswith('# Warning:'):
            sID, sMessage = extract_id_and_message(sLine)
            oWarning = warning.LogWarning(sID, sMessage, None, iLineNumber + 1)
            oReturn.add_warning(oWarning)
    return oReturn


def extract_id_and_message(sLine):
    sText = extract_text_after_keyword(sLine)
    if not has_id_separator(sText):
        return vendor_utils.NO_ID, sText.strip()

    sId, sMessage = sText.split(':', 1)
    sId = remove_surrounding_brackets(sId.strip())
    if contains_spaces(sId):
        return vendor_utils.NO_ID, sText.strip()

    return sId, sMessage.strip()


def extract_text_after_keyword(sLine):
    return sLine.split(':', 1)[1]


def has_id_separator(sText):
    return ':' in sText


def contains_spaces(sText):
    return ' ' in sText


def remove_surrounding_brackets(sId):
    if not is_surrounded_by_brackets(sId):
        return sId
    return sId[1:-1]


def is_surrounded_by_brackets(sId):
    return sId.startswith('[') and sId.endswith(']')

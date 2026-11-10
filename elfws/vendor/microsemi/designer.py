
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

    for iIndex, sLine in enumerate(lFile):
        if is_warning_start(sLine):
            lContinuationLines = collect_continuation_lines(lFile, iIndex + 1)
            oReturn.add_warning(build_warning(sLine, lContinuationLines, iIndex + 1))

    return oReturn


def is_warning_start(sLine):
    return sLine.startswith('Warning:')


def collect_continuation_lines(lFile, iStartIndex):
    lReturn = []
    for sLine in lFile[iStartIndex:]:
        if not is_continuation(sLine):
            break
        lReturn.append(sLine)
    return lReturn


def is_continuation(sLine):
    return sLine.startswith(' ')


def build_warning(sFirstLine, lContinuationLines, iLineNumber):
    sID, sMessage = extract_id_and_message(sFirstLine)
    for sLine in lContinuationLines:
        sMessage += ' ' + sLine.strip()
    return warning.LogWarning(sID, sMessage, None, iLineNumber)


def extract_id_and_message(sLine):
    sText = extract_text_after_keyword(sLine)
    if not has_id_separator(sText):
        return vendor_utils.NO_ID, sText.strip()

    sId, sMessage = sText.split(':', 1)
    if contains_spaces(sId.strip()):
        return vendor_utils.NO_ID, sText.strip()

    return sId.strip(), sMessage.strip()


def extract_text_after_keyword(sLine):
    return sLine.split(':', 1)[1]


def has_id_separator(sText):
    return ':' in sText


def contains_spaces(sText):
    return ' ' in sText

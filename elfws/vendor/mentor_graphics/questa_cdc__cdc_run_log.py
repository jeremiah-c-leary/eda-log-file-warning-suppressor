
from elfws import warning
from elfws import warning_list

from elfws.vendor import utils as vendor_utils
from elfws.vendor.mentor_graphics import utils as cdc_utils

LAST_HEADER_LINE_INDEX = 20


def get_vendor():
    return ['Mentor Graphics']


def get_tool_name():
    return 'questa_cdc'


def is_logfile(lFile):
    fToolFound = False
    for iLineNumber, sLine in enumerate(lFile):
        if fToolFound:
           if sLine.lstrip().startswith('-tool cdc'):
               return True
           if sLine.lstrip().startswith('Executing Command : cdc run'):
               return True
        if sLine.startswith('# Questa Static Verification System'):
            fToolFound = True
        if iLineNumber == LAST_HEADER_LINE_INDEX:
            break
    return False


def extract_warnings(lFile):
    oReturn = warning_list.WarningList()

    cdc_utils.extract_cdc_violations(oReturn, lFile)
    cdc_utils.extract_cdc_cautions(oReturn, lFile)
    cdc_utils.extract_cdc_evaluations(oReturn, lFile)
    extract_message_warnings(oReturn, lFile)
    extract_message_errors(oReturn, lFile)

    return oReturn


def extract_message_warnings(oReturn, lFile):
    fWarningSectionFound = False
    sID = 'warning_check'
    for iLineNumber, sLine in enumerate(lFile):
        if vendor_utils.sequence_of_lines_starts_with(iLineNumber, lFile, ['Message Summary', '----', 'Count', '----']):
            fWarningSectionFound = True
            continue
        if fWarningSectionFound:
            if sLine == '':
                break
            lLine = sLine.split()
            if is_message_type(lLine, 'Warning'):
               oWarning = warning.LogWarning(sID, sLine, None, iLineNumber + 1)
               oReturn.add_warning(oWarning) 


def extract_message_errors(oReturn, lFile):
    fWarningSectionFound = False
    sID = 'error_check'
    for iLineNumber, sLine in enumerate(lFile):
        if vendor_utils.sequence_of_lines_starts_with(iLineNumber, lFile, ['Message Summary', '----', 'Count', '----']):
            fWarningSectionFound = True
            continue
        if fWarningSectionFound:
            if sLine == '':
                break
            lLine = sLine.split()
            if is_message_type(lLine, 'Error'):
               oWarning = warning.LogWarning(sID, sLine, None, iLineNumber + 1)
               oReturn.add_warning(oWarning) 


def is_message_type(lLine, sType):
    if not has_message_type_column(lLine):
        return False
    return lLine[1] == sType


def has_message_type_column(lLine):
    return len(lLine) > 1


from elfws import warning
from elfws import warning_list

LAST_HEADER_LINE_INDEX = 10


def get_vendor():
    return ['Mentor Graphics']


def get_tool_name():
    return 'questa_lint'


def is_logfile(lFile):
    for iLineNumber, sLine in enumerate(lFile):
        if sLine.startswith('Questa Lint  Version'):
            return True
        if iLineNumber == LAST_HEADER_LINE_INDEX:
            return False
    return False


def extract_warnings(lFile):
    oReturn = warning_list.WarningList()

    fWarningFound = False
    fWarningSectionFound = False
    sID = 'elfws'
    for iLineNumber, sLine in enumerate(lFile):
        if sLine.startswith('Section 2'):
            fWarningSectionFound = True
            
        if fWarningSectionFound:
            if sLine.startswith('| Info'):
                break
            if sLine.startswith('Check:'):
                lLine = sLine.split()
                sID = lLine[1]
                continue
            if fWarningFound and sLine == '':
                fWarningFound = False
                oWarning = warning.LogWarning(sID, sMessage, None, iWarningLineNumber)
                oReturn.add_warning(oWarning)

            if fWarningFound:
                sMessage += ' ' + sLine
            if sLine.startswith(sID):
                fWarningFound = True
                sMessage = sLine[len(sID) + 2:]
                iWarningLineNumber = iLineNumber + 1

    if fWarningFound:
        oReturn.add_warning(warning.LogWarning(sID, sMessage, None, iWarningLineNumber))

    return oReturn

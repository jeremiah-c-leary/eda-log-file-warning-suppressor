
from elfws import warning
from elfws import warning_list

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
            iColon1Index = sLine.find(':')
            iColon2Index = sLine.find(':', iColon1Index+1)
            sID = sLine[iColon1Index+1:iColon2Index].strip()
            sMessage = sLine[iColon2Index+1:].strip()
            oWarning = warning.LogWarning(sID, sMessage, None, iLineNumber + 1)
            oReturn.add_warning(oWarning)
    return oReturn

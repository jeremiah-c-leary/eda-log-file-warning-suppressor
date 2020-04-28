
from elfws import warning
from elfws import warning_list


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
        if iLineNumber == 10:
            return False
    return False


def extract_warnings(lFile):
    oReturn = warning_list.create()

    fWarningFound = False
    for iLineNumber, sLine in enumerate(lFile):
        if sLine.startswith('# Warning:'):
            iColon1Index = sLine.find(':')
            iColon2Index = sLine.find(':', iColon1Index+1)
            sID = sLine[iColon1Index+1:iColon2Index].strip()
            sID = sID[1:-1]
            if ' ' in sID:
                sID = 'NO_ID'
                sMessage = sLine[iColon1Index+1:].strip()
            else:
                sMessage = sLine[iColon2Index+1:].strip()
            oWarning = warning.create(sID, sMessage, None, iLineNumber + 1)
            oReturn.add_warning(oWarning)
    return oReturn

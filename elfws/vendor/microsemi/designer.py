
from elfws import warning
from elfws import warning_list


def extract_warnings(lFile):
    oReturn = warning_list.create()

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
            iColon1Index = sLine.find(':')
            iColon2Index = sLine.find(':', iColon1Index+1)
            if iColon2Index == -1:
                sID = 'NO_ID'
                sMessage = sLine[iColon1Index+1:].strip()
            else:
                sID = sLine[iColon1Index+1:iColon2Index].strip()
                sMessage = sLine[iColon2Index+1:].strip()
                if ' ' in sID:
                    sID = 'NO_ID'
                    sMessage = sLine[iColon1Index+1:].strip()
            oWarning = warning.create(sID, sMessage, None, iLineNumber + 1)
    return oReturn

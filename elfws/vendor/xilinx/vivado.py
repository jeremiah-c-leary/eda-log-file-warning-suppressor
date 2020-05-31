from elfws import warning
from elfws import warning_list


def get_vendor():
    return ['Xilinx']


def get_tool_name():
    return 'vivado'


def is_logfile(lFile):
    for iLineNumber, sLine in enumerate(lFile):
        if sLine.startswith('****** Vivado'):
            return True
        if sLine.startswith('# Vivado '):
            return True
        if iLineNumber == 200:
            return False
    return False


def extract_warnings(lFile):
    oReturn = warning_list.create()

    fWarningFound = False
    for iLineNumber, sLine in enumerate(lFile):
        # Clear the warning found flag to keep track of multiline warnings
        if not sLine.startswith(' ') and fWarningFound:
            fWarningFound = False
            oReturn.add_warning(oWarning)
        if sLine.startswith(' ') and fWarningFound:
            oWarning.message += ' ' + sLine.strip()
        if sLine.startswith('WARNING:') or sLine.startswith('CRITICAL WARNING'):
            fWarningFound = True
            iOpenBracketIndex = sLine.find('[')
            iCloseBracketIndex = sLine.find(']', iOpenBracketIndex+1)
            sID = sLine[iOpenBracketIndex+1:iCloseBracketIndex].strip()
            sMessage = sLine[iCloseBracketIndex+1:].strip()
            oWarning = warning.create(sID, sMessage, None, iLineNumber + 1)
    return oReturn

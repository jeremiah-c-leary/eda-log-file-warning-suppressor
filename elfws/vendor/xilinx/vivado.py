from elfws import warning
from elfws import warning_list

LAST_HEADER_LINE_INDEX = 200


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
    return sLine.startswith('WARNING:') or sLine.startswith('CRITICAL WARNING')


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
    iOpenBracketIndex = sLine.find('[')
    iCloseBracketIndex = sLine.find(']', iOpenBracketIndex+1)
    sID = sLine[iOpenBracketIndex+1:iCloseBracketIndex].strip()
    sMessage = sLine[iCloseBracketIndex+1:].strip()
    return sID, sMessage

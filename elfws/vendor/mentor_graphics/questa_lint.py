
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

    for sCheckId, lCheckLines in check_blocks(warning_section(lFile)):
        for oWarning in extract_check_warnings(sCheckId, lCheckLines):
            oReturn.add_warning(oWarning)

    return oReturn


def warning_section(lFile):
    '''
    Returns the lines between the Section 2 heading and the Info section.

    Parameters:

      lFile : (list of strings)

    Returns: (list of tuples) line number, line
    '''
    iStartIndex = index_of_first_line_starting_with(lFile, 'Section 2', 0)
    iEndIndex = index_of_first_line_starting_with(lFile, '| Info', iStartIndex)
    return [(iIndex + 1, lFile[iIndex]) for iIndex in range(iStartIndex, iEndIndex)]


def index_of_first_line_starting_with(lFile, sPrefix, iStartIndex):
    for iIndex in range(iStartIndex, len(lFile)):
        if lFile[iIndex].startswith(sPrefix):
            return iIndex
    return len(lFile)


def check_blocks(lSection):
    '''
    Splits the warning section into the lines following each Check heading.

    Parameters:

      lSection : (list of tuples) line number, line

    Returns: (generator of tuples) check id, lines below the Check heading
    '''
    lCheckIndexes = [iIndex for iIndex, (iLineNumber, sLine) in enumerate(lSection) if is_check_line(sLine)]
    lBlockEnds = lCheckIndexes[1:] + [len(lSection)]
    for iCheckIndex, iBlockEnd in zip(lCheckIndexes, lBlockEnds):
        yield check_id(lSection[iCheckIndex][1]), lSection[iCheckIndex + 1:iBlockEnd]


def extract_check_warnings(sCheckId, lCheckLines):
    lReturn = []
    for iIndex, (iLineNumber, sLine) in enumerate(lCheckLines):
        if is_warning_start(sLine, sCheckId):
            lReturn.append(build_warning(sCheckId, sLine, continuation_lines(lCheckLines, iIndex + 1, sCheckId), iLineNumber))
    return lReturn


def build_warning(sCheckId, sFirstLine, lContinuationLines, iLineNumber):
    sMessage = sFirstLine[len(sCheckId) + 1:].lstrip()
    for sLine in lContinuationLines:
        sMessage += ' ' + sLine
    return warning.LogWarning(sCheckId, sMessage, None, iLineNumber)


def continuation_lines(lCheckLines, iStartIndex, sCheckId):
    lReturn = []
    for iLineNumber, sLine in lCheckLines[iStartIndex:]:
        if is_end_of_message(sLine, sCheckId):
            break
        lReturn.append(sLine)
    return lReturn


def is_end_of_message(sLine, sCheckId):
    return sLine == '' or is_warning_start(sLine, sCheckId)


def is_warning_start(sLine, sCheckId):
    return sLine.startswith(sCheckId + ':')


def is_check_line(sLine):
    return sLine.startswith('Check:')


def check_id(sLine):
    return sLine.split()[1]

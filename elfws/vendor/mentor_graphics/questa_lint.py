
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

    lWarningSection = warning_section(lFile)
    for sCheckId, lCheckLines in check_blocks(lWarningSection):
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
    Groups the warning section into one block per Check heading.

    Lines before the first Check heading do not belong to any block.

    Parameters:

      lSection : (list of tuples) line number, line

    Returns: (list of tuples) check id, lines below the Check heading
    '''
    lBlocks = []
    for iLineNumber, sLine in lSection:
        if is_check_line(sLine):
            lBlocks.append((check_id(sLine), []))
            continue

        if has_blocks(lBlocks):
            lCurrentCheckLines = lBlocks[-1][1]
            lCurrentCheckLines.append((iLineNumber, sLine))

    return lBlocks


def is_check_line(sLine):
    return sLine.startswith('Check:')


def check_id(sLine):
    return sLine.split()[1]


def has_blocks(lBlocks):
    return len(lBlocks) > 0


def extract_check_warnings(sCheckId, lCheckLines):
    lReturn = []
    for iIndex, (iLineNumber, sLine) in enumerate(lCheckLines):
        if is_warning_start(sLine, sCheckId):
            lContinuationLines = continuation_lines(lCheckLines, iIndex + 1, sCheckId)
            lReturn.append(build_warning(sCheckId, sLine, lContinuationLines, iLineNumber))
    return lReturn


def is_warning_start(sLine, sCheckId):
    return sLine.startswith(sCheckId + ':')


def continuation_lines(lCheckLines, iStartIndex, sCheckId):
    lReturn = []
    for iLineNumber, sLine in lCheckLines[iStartIndex:]:
        if is_end_of_message(sLine, sCheckId):
            break
        lReturn.append(sLine)
    return lReturn


def is_end_of_message(sLine, sCheckId):
    return sLine == '' or is_warning_start(sLine, sCheckId)


def build_warning(sCheckId, sFirstLine, lContinuationLines, iLineNumber):
    sMessage = sFirstLine[len(sCheckId) + 1:].lstrip()
    for sLine in lContinuationLines:
        sMessage += ' ' + sLine
    return warning.LogWarning(sCheckId, sMessage, None, iLineNumber)

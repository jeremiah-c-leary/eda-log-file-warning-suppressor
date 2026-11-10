
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

    lWarningSection = extract_warning_section(lFile)
    for sLintCheckId, lLintCheckLines in group_lines_by_lint_check(lWarningSection):
        for oWarning in extract_lint_check_warnings(sLintCheckId, lLintCheckLines):
            oReturn.add_warning(oWarning)

    return oReturn


def extract_warning_section(lFile):
    '''
    Returns the lines between the Section 2 heading and the Info section.

    Parameters:

      lFile : (list of strings)

    Returns: (list of tuples) line number, line
    '''
    iStartIndex = find_index_of_first_line_starting_with(lFile, 'Section 2', 0)
    iEndIndex = find_index_of_first_line_starting_with(lFile, '| Info', iStartIndex)
    return [(iIndex + 1, lFile[iIndex]) for iIndex in range(iStartIndex, iEndIndex)]


def find_index_of_first_line_starting_with(lFile, sPrefix, iStartIndex):
    for iIndex in range(iStartIndex, len(lFile)):
        if lFile[iIndex].startswith(sPrefix):
            return iIndex
    return len(lFile)


def group_lines_by_lint_check(lWarningSection):
    '''
    Groups the lines of the warning section by the lint check heading above them.

    Lines before the first lint check heading do not belong to any lint check.

    Parameters:

      lWarningSection : (list of tuples) line number, line

    Returns: (list of tuples) lint check id, lines below the lint check heading
    '''
    lLintChecks = []
    for iLineNumber, sLine in lWarningSection:
        if is_lint_check_heading(sLine):
            lLintChecks.append((extract_lint_check_id(sLine), []))
            continue

        if has_found_a_lint_check(lLintChecks):
            lCurrentLintCheckLines = lLintChecks[-1][1]
            lCurrentLintCheckLines.append((iLineNumber, sLine))

    return lLintChecks


def is_lint_check_heading(sLine):
    return sLine.startswith('Check:')


def extract_lint_check_id(sLine):
    return sLine.split()[1]


def has_found_a_lint_check(lLintChecks):
    return len(lLintChecks) > 0


def extract_lint_check_warnings(sLintCheckId, lLintCheckLines):
    lReturn = []
    for iIndex, (iLineNumber, sLine) in enumerate(lLintCheckLines):
        if is_warning_start(sLine, sLintCheckId):
            lContinuationLines = collect_continuation_lines(lLintCheckLines, iIndex + 1, sLintCheckId)
            lReturn.append(build_warning(sLintCheckId, sLine, lContinuationLines, iLineNumber))
    return lReturn


def is_warning_start(sLine, sLintCheckId):
    return sLine.startswith(sLintCheckId + ':')


def collect_continuation_lines(lLintCheckLines, iStartIndex, sLintCheckId):
    lReturn = []
    for iLineNumber, sLine in lLintCheckLines[iStartIndex:]:
        if is_end_of_message(sLine, sLintCheckId):
            break
        lReturn.append(sLine)
    return lReturn


def is_end_of_message(sLine, sLintCheckId):
    return sLine == '' or is_warning_start(sLine, sLintCheckId)


def build_warning(sLintCheckId, sFirstLine, lContinuationLines, iLineNumber):
    sMessage = sFirstLine[len(sLintCheckId) + 1:].lstrip()
    for sLine in lContinuationLines:
        sMessage += ' ' + sLine
    return warning.LogWarning(sLintCheckId, sMessage, None, iLineNumber)

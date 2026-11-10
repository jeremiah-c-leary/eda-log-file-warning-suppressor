
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
    lWarningSection = extract_warning_section(lFile)
    lLintChecks = extract_lint_checks(lWarningSection)
    return create_warning_list(lLintChecks)


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


def extract_lint_checks(lWarningSection):
    '''
    Creates a lint check for each lint check heading in the warning section.

    Each lint check holds the lines below its heading.
    Lines before the first lint check heading do not belong to any lint check.

    Parameters:

      lWarningSection : (list of tuples) line number, line

    Returns: (list of LintCheck objects)
    '''
    lLintChecks = []
    for iLineNumber, sLine in lWarningSection:
        if is_lint_check_heading(sLine):
            lLintChecks.append(LintCheck(extract_lint_check_id(sLine)))
            continue

        if has_found_a_lint_check(lLintChecks):
            lLintChecks[-1].add_line(iLineNumber, sLine)

    return lLintChecks


def is_lint_check_heading(sLine):
    return sLine.startswith('Check:')


def extract_lint_check_id(sLine):
    return sLine.split()[1]


def has_found_a_lint_check(lLintChecks):
    return len(lLintChecks) > 0


def create_warning_list(lLintChecks):
    oReturn = warning_list.WarningList()
    for oLintCheck in lLintChecks:
        for oWarning in oLintCheck.extract_warnings():
            oReturn.add_warning(oWarning)
    return oReturn


class LintCheck():
    '''
    A Questa Lint check and the lines reported below its heading.
    '''

    def __init__(self, sId):
        self.sId = sId
        self.lLines = []

    def add_line(self, iLineNumber, sLine):
        self.lLines.append((iLineNumber, sLine))

    def extract_warnings(self):
        lReturn = []
        for iIndex, (iLineNumber, sLine) in enumerate(self.lLines):
            if self.is_warning_start(sLine):
                lContinuationLines = self.collect_continuation_lines(iIndex + 1)
                lReturn.append(self.build_warning(sLine, lContinuationLines, iLineNumber))
        return lReturn

    def is_warning_start(self, sLine):
        return sLine.startswith(self.sId + ':')

    def collect_continuation_lines(self, iStartIndex):
        lReturn = []
        for iLineNumber, sLine in self.lLines[iStartIndex:]:
            if self.is_end_of_message(sLine):
                break
            lReturn.append(sLine)
        return lReturn

    def is_end_of_message(self, sLine):
        return sLine == '' or self.is_warning_start(sLine)

    def build_warning(self, sFirstLine, lContinuationLines, iLineNumber):
        sMessage = sFirstLine[len(self.sId) + 1:].lstrip()
        for sLine in lContinuationLines:
            sMessage += ' ' + sLine
        return warning.LogWarning(self.sId, sMessage, None, iLineNumber)

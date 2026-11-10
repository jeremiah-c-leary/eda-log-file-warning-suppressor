
from datetime import datetime

from elfws import version

REPORT_WIDTH = 80
MINIMUM_ID_COLUMN_WIDTH = 15
LINE_NUMBER_COLUMN_WIDTH = 6
CELL_PADDING = 2
NUMBER_OF_COLUMN_SEPARATORS = 2
STATISTIC_LABEL_WIDTH = 22
STATISTIC_VALUE_WIDTH = 5


def print_results(oResults):
    '''
    Displays results of a subcommand to the terminal window.

    Parameters:

      oResults : (SuppressionResults object)

    Returns : None
    '''
    lLines = build_results_lines(oResults)
    print_lines(lLines)


def build_results_lines(oResults):
    lReturn = []
    lReturn.extend(build_header(oResults.sLogFileName, oResults.sSuppressionFileName))
    lUnsuppressedWarnings = oResults.oWarnList.get_unsuppressed_warnings()
    lReturn.extend(build_warning_table(lUnsuppressedWarnings))
    lReturn.extend(build_report_summary_section(oResults))
    return lReturn


def print_lines(lLines):
    for sLine in lLines:
        print(sLine)


def build_header(sLogFileName, sSuppressionFileName):
    '''
    Creates the header which will be displayed to the screen.

    Parameters:

      sLogFileName : (string)

      sSuppressionFileName : (string)

    Returns: (list of strings)
    '''
    lReturn = []
    lReturn.append('='*REPORT_WIDTH)
    lReturn.append('ELFWS version         : ' + version.version)
    lReturn.append('Date                  : ' + str(datetime.now()))
    lReturn.append('Log file              : ' + sLogFileName)
    lReturn.append('Suppression Rule File : ' + sSuppressionFileName)
    lReturn.append('')

    return lReturn


def build_warning_table(lWarningList, iIndent=0):
    '''
    Creates the warning table given a warning list.

    Parameters:

      lWarningList : (list of warning objects)

    Returns: (list of strings)
    '''
    if len(lWarningList) == 0:
        return []

    iWarningIdLength = find_maximum_id_length(lWarningList)
    lReturn = []
    lReturn.append(build_table_row_seperator(iWarningIdLength, iIndent))
    lReturn.append(build_table_header_format_string(iWarningIdLength, iIndent).format('ID', 'Line #', 'Warning Message'))
    lReturn.append(build_table_row_seperator(iWarningIdLength, iIndent))
    for oWarning in lWarningList:
        lReturn.append(build_table_row_format_string(iWarningIdLength, iIndent).format(oWarning.get_id(), oWarning.get_linenumber(), oWarning.get_message()))
    lReturn.append(build_table_row_seperator(iWarningIdLength, iIndent))
    lReturn.append('')

    return lReturn


def build_table_row_seperator(iFirstColumnLength, iIndent=0):
    '''
    Creates a row separator for the warning table.

    Parameters :

      iFirstColumnLength : (integer)

      iIndent : (integer)

    Returns: (string)
    '''
    sIndent = ' '*iIndent
    iIdCellWidth = calculate_id_column_width(iFirstColumnLength) + CELL_PADDING
    iLineNumberCellWidth = LINE_NUMBER_COLUMN_WIDTH + CELL_PADDING
    iMessageCellWidth = REPORT_WIDTH - iIndent - iIdCellWidth - iLineNumberCellWidth - NUMBER_OF_COLUMN_SEPARATORS
    return sIndent + '-'*iIdCellWidth + '+' + '-'*iLineNumberCellWidth + '+' + '-'*iMessageCellWidth


def calculate_id_column_width(iIdLength):
    return max(MINIMUM_ID_COLUMN_WIDTH, iIdLength)


def build_stat_line(sString, iNumber):
    '''
    Creates a line for the statistics in the footer.

    Parameters:

      sString : (string)

      iNumber : (integer)

    Returns : (string)
    '''
    sFormat = '    {0:<' + str(STATISTIC_LABEL_WIDTH) + 's} : {1:' + str(STATISTIC_VALUE_WIDTH) + 'd}'
    return sFormat.format(sString, iNumber)


def build_table_of_contents():
    '''
    Creates a table of contents for the report.

    Returns: (list of strings)
    '''
    lReturn = []
    lReturn.append('Table of Contents:')
    lReturn.append('')
    lReturn.append('  1.  Unsuppressed Warnings')
    lReturn.append('  2.  Suppressed Warnings')
    lReturn.append('  3.  Unused Suppression Rules')
    lReturn.append('  4.  Warnings Under Investigation')
    lReturn.append('  5.  Warnings Suppressed by Multiple Rules')
    lReturn.append('  6.  Summary')
    lReturn.append('')

    return lReturn


def build_report_section_divider(sTitle):
    '''
    Creates a section divider for the report.

    Parameters:

      sTitle : (string)

    Returns:  (list of strings)
    '''
    lReturn = []
    lReturn.append('-'*REPORT_WIDTH)
    lReturn.append(' ' + sTitle)
    lReturn.append('-'*REPORT_WIDTH)
    lReturn.append('')

    return lReturn


def build_suppressed_warning_header(oSuppression, iIndent=0):
    '''
    Creates a header for a suppressed warning section in the report.

    Parameters:

      oSuppression : (suppression object)

    Return:  (list of strings)
    '''
    sIndent = ' '*iIndent
    lReturn = []
    lReturn.append(sIndent + '~'*(REPORT_WIDTH - iIndent))
    lReturn.append(sIndent + 'Suppression Author  : ' + oSuppression.get_author())
    lReturn.append(sIndent + 'Suppression Comment : ' + oSuppression.get_comment())
    lReturn.append(sIndent + 'Suppression Rule    : ' + oSuppression.get_message())
    lReturn.append('')

    return lReturn


def build_suppressed_warning_table(oSuppression, iIndent=0):
    '''
    Creates a table of suppressed messages for a given suppression rule.

    Parameters:

      oSuppression : (suppression object)

    Return: (list of strings)
    '''
    return build_warning_table(oSuppression.get_suppressed_warnings(), iIndent)


def build_suppression_item(oSuppression, iIndent=0):
    '''
    Creates a formatted report of suppression data.

    Parameters:

      oSuppression : (suppression object)

      iIndent : (integer)

    Return: (list of strings)
    '''
    sIndent = ' '*iIndent
    lReturn = []
    lReturn.append(sIndent + 'Warning ID : ' + oSuppression.get_warning_id())
    lReturn.append(sIndent + 'Author     : ' + oSuppression.get_author())
    lReturn.append(sIndent + 'Rule       : .*' + oSuppression.get_message() + '.*')
    lReturn.append(sIndent + 'Comment    : ' + oSuppression.get_comment())
    lReturn.append('')

    return lReturn


def build_multiply_suppressed_warning_header(oWarning, iIndent=0):
    '''
    Creates a header for a warning that has been suppressed by more than one suppression rule.

    Parameters :

      oWarning : (warning object)

    Returns (list of strings)
    '''
    sIndent = ' '*iIndent
    lReturn = []
    lReturn.append(sIndent + '~'*(REPORT_WIDTH - iIndent))
    lReturn.append(sIndent + 'Warning ID  : ' + oWarning.get_id())
    lReturn.append(sIndent + 'Line Number : ' + str(oWarning.get_linenumber()))
    lReturn.append(sIndent + 'Message     : ' + oWarning.get_message())
    lReturn.append('')

    return lReturn


def build_report_summary_section(oResults):
    '''
    Creates the summary section of the report.

    Parameters:

      oResults : (SuppressionResults object)

    Returns: (list of string)
    '''
    oSupList = oResults.oSupList
    oWarnList = oResults.oWarnList
    lReturn = []
    lReturn.append('  Suppression Rules')
    lReturn.append(build_stat_line('Total', oSupList.get_number_of_suppressions()))
    lReturn.append(build_stat_line('Unused', len(oSupList.get_suppressions_which_did_not_suppress_a_warning())))
    lReturn.append('')
    lReturn.append('  Warnings')
    lReturn.append(build_stat_line('Total', oWarnList.get_number_of_warnings()))
    lReturn.append(build_stat_line('Suppressed', len(oWarnList.get_suppressed_warnings())))
    lReturn.append(build_stat_line('Unsuppressed', len(oWarnList.get_unsuppressed_warnings())))
    lReturn.append(build_stat_line('Under Investigation', len(oWarnList.get_investigate_warnings())))
    lReturn.append(build_stat_line('Multiply Suppressed', len(oWarnList.get_warnings_suppressed_by_multiple_rules())))
    lReturn.append('')
    lReturn.append('='*REPORT_WIDTH)

    return lReturn


def find_maximum_id_length(lWarnings):
    '''
    Returns the maximum length of warnings in a list.

    Parameters :

      lWarnings : (list of warnings)

    Returns : (integer)
    '''
    iReturn = 0
    for oWarning in lWarnings:
        iReturn = max(iReturn, len(oWarning.get_id()))
    return iReturn


def build_table_header_format_string(iIdLength, iIndent):
    '''
    Returns the format string for a table row.

    Parameters :

      iIdLength : (integer)

      iIndent : (integer)

    Returns : (string)
    '''
    return build_table_format_string(iIdLength, iIndent, 's')


def build_table_row_format_string(iIdLength, iIndent):
    '''
    Returns the format string for a table row.

    Parameters :

      iIdLength : (integer)

      iIndent : (integer)

    Returns : (string)
    '''
    return build_table_format_string(iIdLength, iIndent, 'd')


def build_table_format_string(iIdLength, iIndent, sLineNumberType):
    '''
    Returns the format string shared by the table header and rows.

    Parameters :

      iIdLength : (integer)

      iIndent : (integer)

      sLineNumberType : (string) format type of the line number column, 's' for the header and 'd' for rows

    Returns : (string)
    '''
    sReturn = iIndent * ' '
    sReturn += ' {0:<' + str(calculate_id_column_width(iIdLength)) + 's} | {1:' + str(LINE_NUMBER_COLUMN_WIDTH) + sLineNumberType + '} | {2:s}'
    return sReturn

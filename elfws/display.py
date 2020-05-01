
from datetime import datetime

from elfws import version


def results(sLogFileName, sSuppressionFileName, oSupList, oWarnList):
    '''
    Displays results of a subcommand to the terminal window.

    Parameters:

      sLogFileName: (string)
      sSuppressionFileName : (string)
      oSupList : (suppression list object)
      oWarnList : (warning list object)

    Returns : None
    '''
    lPrint = build_header(sLogFileName, sSuppressionFileName)
    lWarnings = oWarnList.get_unsuppressed_warnings()
    lPrint.extend(build_warning_table(lWarnings))
    lPrint.extend(build_report_summary_section(oWarnList, oSupList))
    for sLine in lPrint:
        print(sLine)


def build_header(sLogFileName, sSuppressionFileName):
    '''
    Creates the header which will be displayed to the screen.

    Parameters:

      sLogFileName : (string)

      sSuppressionFileName : (string)

    Returns: (list of strings)
    '''
    sDateTime = str(datetime.now())
    lReturn = []
    lReturn.append('='*80)
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
    sIndent = ' '*iIndent
    lReturn = []
    if len(lWarningList) > 0:
        lReturn.append(build_table_row_seperator(iIndent))
        lReturn.append(sIndent + ' {0:<15s} | {1:6s} | {2:s}'.format('ID', 'Line #', 'Warning Message'))
        lReturn.append(build_table_row_seperator(iIndent))
        for oWarning in lWarningList:
            lReturn.append(sIndent + ' {0:<15s} | {1:6d} | {2:s}'.format(oWarning.get_id(), oWarning.get_linenumber(), oWarning.get_message()))
        lReturn.append(build_table_row_seperator(iIndent))
        lReturn.append('')

    return lReturn


def build_table_row_seperator(iIndent=0):
    '''
    Creates a row separator for the warning table.

    Returns: (string)
    '''
    sIndent = ' '*iIndent
    return sIndent + '-'*17 + '+' + '-'*8 + '+' + '-'*(80 - 20 - 1 - 5 - 1 - iIndent)


def build_stat_line(sString, iNumber):
    '''
    Creates a line for the statistics in the footer.

    Parameters:

      sString : (string)

      iNumber : (integer)

    Returns : (string)
    '''
    return '    {0:<22s} : {1:5d}'.format(sString, iNumber)


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
    lReturn.append('  4.  Warnings Suppressed by Multiple Rules')
    lReturn.append('  5.  Summary')
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
    lReturn.append('-'*80)
    lReturn.append(' ' + sTitle)
    lReturn.append('-'*80)
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
    lReturn.append(sIndent + '~'*(80 - iIndent))
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
    sIndent = ' '*iIndent
    lReturn = []
    lReturn.append(build_table_row_seperator(iIndent))
    lReturn.append(sIndent + ' {0:<15s} | {1:6s} | {2:s}'.format('ID', 'Line #', 'Warning Message'))
    lReturn.append(build_table_row_seperator(iIndent))
    for oWarning in oSuppression.get_suppressed_warnings():
        lReturn.append(sIndent + ' {0:<15s} | {1:6d} | {2:s}'.format(oWarning.get_id(), oWarning.get_linenumber(), oWarning.get_message()))
    lReturn.append(build_table_row_seperator(iIndent))
    lReturn.append('')

    return lReturn


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
    lReturn.append(sIndent + '~'*(80 - iIndent))
    lReturn.append(sIndent + 'Warning ID  : ' + oWarning.get_id())
    lReturn.append(sIndent + 'Line Number : ' + str(oWarning.get_linenumber()))
    lReturn.append(sIndent + 'Message     : ' + oWarning.get_message())
    lReturn.append('')

    return lReturn


def build_report_summary_section(oWarnList, oSupList):
    '''
    Creates the summary section of the report.

    Parameters:

      oWarnList : (warning list object)

      oSupList : (suppression list object)

    Returns: (list of string)
    '''
    lReturn = []
    sFormatString = '    {0:<22s} : {1:5d}'
    lReturn.append('  Suppression Rules')
    lReturn.append(build_stat_line('Total', oSupList.get_number_of_suppressions()))
    lReturn.append(build_stat_line('Unused', len(oSupList.get_suppressions_which_did_not_suppress_a_warning())))
    lReturn.append('')
    lReturn.append('  Warnings')
    lReturn.append(build_stat_line('Total', oWarnList.get_number_of_warnings()))
    lReturn.append(build_stat_line('Suppressed', len(oWarnList.get_suppressed_warnings())))
    lReturn.append(build_stat_line('Unsuppressed', len(oWarnList.get_unsuppressed_warnings())))
    lReturn.append(build_stat_line('Multiply Suppressed', len(oWarnList.get_warnings_suppressed_by_multiple_rules())))
    lReturn.append('')
    lReturn.append('='*80)

    return lReturn

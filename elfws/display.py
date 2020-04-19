

from elfws import version


def results(sLogFileName, sSuppressionFileName, iTotalWarnings, oWarnList):
    '''
    Displays results of a subcommand to the terminal window.

    Parameters:

      sLogFileName: (string)
      sSuppressionFileName : (string)
      iTotalWarnings : (integer)
      oWarnList : (warning list object)

    Returns : None
    '''
    lPrint = build_header(sLogFileName, sSuppressionFileName)
    lPrint.extend(build_warning_table(oWarnList))
    lPrint.extend(build_footer(iTotalWarnings, oWarnList))
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

    lReturn = []
    lReturn.append('='*80)
    lReturn.append('ELFWS version         : ' + version.version)
    lReturn.append('Log file              : ' + sLogFileName)
    lReturn.append('Suppression Rule File : ' + sSuppressionFileName)
    lReturn.append('')

    return lReturn


def build_warning_table(oWarningList):
    '''
    Creates the warning table given a warning list.

    Parameters:

      oWarningList : (warning list object)

    Returns: (list of strings)
    '''

    lReturn = []
    lReturn.append(build_table_row_seperator())
    lReturn.append(' {0:<15s} | {1:6s} | {2:s}'.format('ID', 'Line #', 'Warning Message'))
    lReturn.append(build_table_row_seperator())
    for oWarning in oWarningList.get_warnings():
        lReturn.append(' {0:<15s} | {1:6d} | {2:s}'.format(oWarning.get_id(), oWarning.get_linenumber(), oWarning.get_message()))
    lReturn.append(build_table_row_seperator())

    return lReturn


def build_table_row_seperator():
    '''
    Creates a row separator for the warning table.

    Returns: (string)
    '''
    return '-'*17 + '+' + '-'*8 + '+' + '-'*(80 - 20 - 1 - 5 - 1)


def build_footer(iTotalWarnings, oWarnList):
    '''
    Creates the footer which will be displayed on the screen.

    Parameters:

      iTotalWarnings: (integer)

      oWarnList: (warning list object)

    Returns: (list of strings)
    '''

    lReturn = []
    lReturn.append('')
    lReturn.append(build_stat_line('Total Warnings', iTotalWarnings))
    lReturn.append(build_stat_line('Suppressed Warnings', iTotalWarnings - oWarnList.get_number_of_warnings()))
    lReturn.append(build_stat_line('Unsuppressed Warnings', oWarnList.get_number_of_warnings()))
    lReturn.append('='*80)

    return lReturn


def build_stat_line(sString, iNumber):
    '''
    Creates a line for the statistics in the footer.

    Parameters:

      sString : (string)

      iNumber : (integer)

    Returns : (string)
    '''
    return '{0:<21s} : {1:5d}'.format(sString, iNumber)

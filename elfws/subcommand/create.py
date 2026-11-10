
import re
import sys
import yaml

from elfws import log_file
from elfws import suppression_results
from elfws.exit_code import ExitCode


def create(oCommandLineArguments):

    lWarnings = extract_warnings_to_suppress(oCommandLineArguments.log_file, oCommandLineArguments.suppression_file)
    dSup = create_suppression_dict(lWarnings)

    with open(oCommandLineArguments.output_suppression_file, 'w') as file:
        yaml.dump(dSup, file)

    sys.exit(ExitCode.SUCCESS)


def extract_warnings_to_suppress(sLogFileName, sSuppressionFileName):
    '''
    Returns the warnings which the existing suppression file does not already suppress.

    Parameters:

      sLogFileName : (string)

      sSuppressionFileName : (string) None when no existing suppression file was given

    Returns: (list of warning objects)
    '''
    if not was_suppression_file_given(sSuppressionFileName):
        oWarnList = log_file.read_warning_list(sLogFileName)
        return oWarnList.get_warnings()

    oResults = suppression_results.apply_suppression_file(sLogFileName, sSuppressionFileName)
    return oResults.oWarnList.get_unsuppressed_warnings()


def was_suppression_file_given(sSuppressionFileName):
    return sSuppressionFileName is not None


def create_suppression_dict(lWarnings):
    '''
    Creates a suppression dictionary that will suppress all warnings in a file.

    Parameters:

      lWarnings : (list of warning objects)

    Returns: (dictionary)
    '''
    dReturn = {}
    dReturn['suppress'] = {}
    dReturn['suppress']['rules'] = {}
    for oWarning in lWarnings:
        sId = oWarning.get_id()
        lKeys = list(dReturn['suppress']['rules'].keys())
        if sId not in lKeys:
            dReturn['suppress']['rules'][sId] = []
        dRule = {}
        dRule['msg'] = escape_regular_expression(oWarning.get_message())
        dRule['author'] = 'elfws'
        dRule['comment'] = '<Add justification why this warning can be suppressed.>'
        dReturn['suppress']['rules'][sId].append(dRule)
    return dReturn


def escape_regular_expression(sString):
    '''
    Escapes regular expression metacharacters so the string matches literally.

    Unlike re.escape, spaces and other ordinary characters are left alone to
    keep the generated suppression file readable.

    Parameters:

      sString : (string)

    Returns: (string)
    '''
    return re.sub(r'([\\.^$*+?{}\[\]|()])', r'\\\1', sString)


import re
import sys
import yaml

from elfws import log_file
from elfws import suppression_file
from elfws.subcommand import suppress
from elfws.exit_code import ExitCode


def create(oCommandLineArguments):

    oWarnList = log_file.read_warning_list(oCommandLineArguments.log_file)

    if oCommandLineArguments.suppression_file is not None:
        oSupList = suppression_file.read_suppression_list(oCommandLineArguments.suppression_file)
        oWarnList = suppress.extract_non_suppressed_warnings(oWarnList, oSupList)

    dSup = create_suppression_dict(oWarnList)

    with open(oCommandLineArguments.output_suppression_file, 'w') as file:
        yaml.dump(dSup, file)

    sys.exit(ExitCode.SUCCESS)


def create_suppression_dict(oWarnList):
    '''
    Creates a suppression dictionary that will suppress all warnings in a file.

    Parameters:

      oWarnList : (warning list object)

    Returns: (dictionary)
    '''
    dReturn = {}
    dReturn['suppress'] = {}
    dReturn['suppress']['rules'] = {}
    for oWarning in oWarnList.get_warnings():
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

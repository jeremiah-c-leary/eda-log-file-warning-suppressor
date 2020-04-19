
import re
import sys
import yaml

from elfws import utils
from elfws.subcommand import suppress


def create(cla):

    lLogFile = utils.read_log_file(cla.log_file)

    oWarnList = utils.create_warning_list(lLogFile, cla.log_file)

    if cla.suppression_file is not None:
        dSup = utils.read_suppression_file(cla.suppression_file)
        oSupList = utils.create_suppression_list(dSup)
        oWarnList = suppress.extract_non_suppressed_warnings(oWarnList, oSupList)

    dSup = create_suppression_dict(oWarnList)

    with open(cla.output_suppression_file, 'w') as file:
        yaml.dump(dSup, file)


def create_suppression_dict(oWarnList):
    '''
    Creates a suppression dictionary that will suppress all warnings in a file.

    Parameters:

      oWarnList : (warning list object)

    Returns: (dictionary)
    '''
    dReturn = {}
    dReturn['suppress'] = {}
    for oWarning in oWarnList.get_warnings():
        sId = oWarning.get_id()
        lKeys = list(dReturn['suppress'].keys())
        if sId not in lKeys:
            dReturn['suppress'][sId] = []
        dRule = {}
        dRule['msg'] = oWarning.get_message()
        dRule['author'] = 'elfws'
        dRule['comment'] = '<Add justification why this warning can be suppressed.>'
        dReturn['suppress'][sId].append(dRule)
    return dReturn

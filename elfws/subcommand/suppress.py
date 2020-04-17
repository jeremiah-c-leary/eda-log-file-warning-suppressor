
import importlib
import sys
import yaml

from elfws import suppression
from elfws import suppression_list


def suppress(cla):

    dSup = read_suppression_file(cla.suppression_file)
    oSupList = create_suppression_list(dSup)

    lLogFile = read_log_file(cla.log_file)

    toolModule = import_vendor_module(cla.vendor, cla.tool)
    oWarnList = toolModule.extract_warnings(lLogFile)
    process_warnings(oWarnList, oSupList)


def read_suppression_file(sFileName):
    '''
    Attempts to read the suppression file and return an list of rules.

    Parameters:

       sFileName : (String)

    Returns:  dictionary
    '''
    with open(sFileName) as yaml_file:
        dReturn = yaml.full_load(yaml_file)

    return dReturn


def create_suppression_list(dSuppression):
    '''
    Processes a given dictionary and returns a suppression list object.

    Parameters:

        dSuppression : (dict)

    Returns:  suppression list object
    '''
    oReturn = suppression_list.create()

    for dID in list(dSuppression['suppress'].keys()):
        for dSup in dSuppression['suppress'][dID]:
            oSupRule = suppression.create(dID, dSup['msg'])
            try:
                oSupRule.author = dSup['author']
            except KeyError:
                oSupRule.auther = None
            try:
                oSupRule.comment= dSup['comment']
            except KeyError:
                oSupRule.comment = None
            oReturn.add_suppression(oSupRule)
    return oReturn


def read_log_file(sFileName):
    lLines = []
    with open(sFileName) as oFile:
        for sLine in oFile:
            lLines.append(sLine)
    oFile.close()
    return lLines


def build_vendor_module_path(sVendor, sTool):
    return '.'.join(['elfws', 'vendor', sVendor.lower(), sTool.lower()])


def import_vendor_module(sVendor, sTool):
    sToolPath = build_vendor_module_path(sVendor, sTool)
    return importlib.import_module(sToolPath)



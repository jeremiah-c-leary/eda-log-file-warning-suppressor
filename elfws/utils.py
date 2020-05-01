
import importlib
import os
import re
import sys
import yaml

from . import suppression
from . import suppression_list


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
            oSupRule = suppression.create(str(dID), dSup['msg'])
            update_suppression_author(oSupRule, dSup)
            update_suppression_comment(oSupRule, dSup)
            oReturn.add_suppression(oSupRule)
    return oReturn


def update_suppression_author(oSupRule, dSup):
    try:
        oSupRule.author = dSup['author']
    except KeyError:
        oSupRule.author = '<None>'


def update_suppression_comment(oSupRule, dSup):
    try:
        oSupRule.comment = dSup['comment']
    except KeyError:
        oSupRule.comment = '<None>'


def read_log_file(sFileName):
    '''
    Reads a log file and strips off line endings.

    Parameters:

      sFileName : (string)

    Returns: (list of strings)
    '''
    lLines = []
    with open(sFileName) as oFile:
        for sLine in oFile:
            lLines.append(sLine.rstrip())
    oFile.close()
    return lLines


def build_vendor_module_path(sVendor, sTool):
    '''
    Creates the path to a vendor's tool module.

    Parameter:

      sVendor : (string)

      sTool   : (string)

    Returns : (string)
    '''
    return '.'.join(['elfws', 'vendor', sVendor.lower(), sTool.lower()])


def import_vendor_module(sVendor, sTool):
    '''
    Imports a module from the elfws/vendor directory based on the parameters.

    For example:
       elfws/vendor/microsemi/designer.py

    Parameters:

      sVendor : (string)

      sTool   : (string)

    Returns : (module)
    '''
    sToolPath = build_vendor_module_path(sVendor, sTool)
    return importlib.import_module(sToolPath)


def get_vendors():
    '''
    Extract the vendors from the vendor directory.

    Parameters:

      None

    Returns: List of directory names
    '''
    lReturn = []
    sVendorPath = os.path.join(os.path.dirname(__file__), 'vendor')
    lListing = os.listdir(sVendorPath)
    for sListing in lListing:
        if sListing.startswith('__'):
            continue
        sPath = os.path.join(os.path.dirname(__file__), sListing)
        if os.path.isdir(os.path.join(os.path.dirname(__file__), 'vendor', sListing)):
            lReturn.append(sListing)
    return lReturn


def get_tools(sVendor):
    '''
    Extract the tools for a vendor.

    Parameters:

      sVendor : (string)

    Returns: list of tool names
    '''
    lReturn = []
    sToolPath = os.path.join(os.path.dirname(__file__), 'vendor', sVendor)
    lListing = os.listdir(sToolPath)
    for sListing in lListing:
        if sListing.startswith('__'):
            continue
        lReturn.append(remove_extension(sListing))
    return lReturn


def remove_extension(sString):
    '''
    Removes the extension from a file name.

    Parameters:

      sString : (string)

    Returns: (string)
    '''
    return os.path.splitext(sString)[0]


def get_vendor_tool_module(lLogFile):
    '''
    Searches for a vendor tool that can parse the given logfile.

    Parameters:

      lLogFile : (list of strings)

    Returns:  (module)
    '''
    for sVendor in get_vendors():
        for sTool in get_tools(sVendor):
            toolModule = import_vendor_module(sVendor, sTool)
            if toolModule.is_logfile(lLogFile):
                return toolModule
    return None


def create_warning_list(lLogFile, sLogFileName):
    '''
    Creates a warning list object from the provided logfile.

    Parameters:

      lLogFile : (string)

    Returns:  (warning list object)
    '''
    try:
        mTool = get_vendor_tool_module(lLogFile)
        return mTool.extract_warnings(lLogFile)
    except AttributeError:
        print('ERROR: File ' + sLogFileName + ' is not recognized as a supported logfile.')
        sys.exit(1)


def apply_suppression_rules_to_warnings(oWarnList, oSupList):
    for oWarning in oWarnList.get_warnings():
        for oSuppression in oSupList.get_suppressions():
            if check_for_match(oWarning, oSuppression):
                oSuppression.add_suppressed_warning(oWarning)
                oWarning.add_suppression_rule(oSuppression)


def check_for_match(oWarning, oSuppression):
    if do_ids_match(oWarning, oSuppression):
        return do_messages_match(oWarning, oSuppression)
    return False


def do_ids_match(oWarning, oSuppression):
    '''
    Checks if the suppression ID matches the warning ID.

    Parameters:

      oWarning : (warning object)

      oSuppression : (suppression object)

    Returns: (boolean)
    '''
    if oWarning.get_id() == oSuppression.get_warning_id():
        return True
    return False


def do_messages_match(oWarning, oSuppression):
    '''
    Checks if the suppression message matches the warning message.

    Parameters:

      oWarning : (warning object)

      oSuppression : (suppression object)

    Returns: (boolean)
    '''
    if re.match('^.*' + oSuppression.get_message(), oWarning.get_message()):
        return True
    return False


def write_file(sFilename, lFile):
    '''
    Writes a list of strings to a file.

    Parameters:

      sFilename : (string)

      lFile : (list of strings)

    Returns: nothing
    '''
    try:
        with open(sFilename, 'w') as oFile:
            for sLine in lFile:
                oFile.write(sLine + '\n')
    except PermissionError as err:
        print(err, "Could not write to file " + sFilename)

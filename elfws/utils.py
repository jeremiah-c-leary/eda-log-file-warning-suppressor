
import importlib
import importlib.util
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
    try:
        with open(sFileName) as yaml_file:
            dReturn = yaml.full_load(yaml_file)
    except Exception as e:
        print(e)
        sys.exit(1)

    if dReturn is None:
        dReturn = {}

    return dReturn


def create_suppression_list(dSuppression):
    '''
    Processes a given dictionary and returns a suppression list object.

    Parameters:

        dSuppression : (dict)

    Returns:  suppression list object
    '''
    oReturn = suppression_list.create()
    try:
        lRules = search_for_suppression_rules(dSuppression['suppress'])
        for oRule in lRules:
            oReturn.add_suppression(oRule)
    except KeyError:
        pass

    return oReturn


def search_for_suppression_rules(dSubDict):
    '''
    This function traverses all keys in a dictionary searching for the key 'rules.'

    NOTE:  This is a recusive function.

    When the key 'rules' is found, extract_suppression_rules is called..
    The rules returned are added to a list which is passed to the calling function.

    Parameters:

        dSubDict : (dict)

    Returns: list of suppression rules
    '''
    lReturn = []
    for dID in list(dSubDict.keys()):
        if dID == 'rules':
            lRules = extract_suppression_rules(dSubDict[dID])
        else:
            lRules = search_for_suppression_rules(dSubDict[dID])
        lReturn.extend(lRules)

    return lReturn


def extract_suppression_rules(dRules):
    '''
    Processes a rule dictionary and return a list of suppression rules.

    Parameters:

        dRules : (dict)

    Returns: list of suppression rules
    '''
    lReturn = []
    try:
        for dID in list(dRules.keys()):
            for dSup in dRules[dID]:
                oSupRule = suppression.create(str(dID), dSup['msg'])
                update_suppression_author(oSupRule, dSup)
                update_suppression_comment(oSupRule, dSup)
                update_suppression_investigate(oSupRule, dSup)
                update_suppression_options(oSupRule, dSup)
                lReturn.append(oSupRule)
    except KeyError:
        pass

    return lReturn


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


def update_suppression_investigate(oSupRule, dSup):
    '''
    Updates the suppression rule based on the investigate key.

    Parameters:

        oSupRule : (suppression rule object)

        dSup : (dictionary)

    Returns: Nothing
    '''
    try:
        if dSup['investigate']:
            oSupRule.investigate = True
    except KeyError:
        oSupRule.investigate = False


def update_suppression_options(oSupRule, dSup):
    '''
    Updates the suppression rule based on the option key.

    Parameters:

        oSupRule : (suppression rule object)

        dSup : (dictionary)

    Returns: Nothing
    '''
    try:
        if dSup['options']:
            oSupRule.set_options(dSup['options'])
    except KeyError:
        oSupRule.set_options([])


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


def import_vendor_module(sToolPath):
    '''
    Imports a module based on the path provided.

    For example:
       elfws/vendor/microsemi/designer.py

    Parameters:

      sToolPath   : (string)

    Returns : (module)
    '''
    spec = importlib.util.spec_from_file_location("tool", sToolPath + '.py')
    tool = importlib.util.module_from_spec(spec)
    sys.modules['tool'] = tool
    spec.loader.exec_module(tool)
    return tool


def get_built_in_vendors():
    '''
    Extract the vendors from the vendor directory.

    Parameters:

      None

    Returns: List of directory names
    '''
    return get_vendors(os.path.join(os.path.dirname(__file__), 'vendor'))


def get_user_defined_vendors():
    '''
    Extract the vendors from the vendor directory.

    Parameters:

      None

    Returns: List of directory names
    '''
    if 'ELFWS_USER_VENDOR_DIR' in os.environ:
        return get_vendors(os.getenv('ELFWS_USER_VENDOR_DIR'))
    return []


def get_vendors(sVendorPath):
    '''
    Extract the vendors from the user defined vendor directory.

    Parameters:

      None

    Returns: List of directory names
    '''
    lReturn = []
    lListing = os.listdir(sVendorPath)
    for sListing in lListing:
        if sListing.startswith('__'):
            continue
        if os.path.isdir(os.path.join(sVendorPath, sListing)):
            lReturn.append(os.path.join(sVendorPath, sListing))
    return lReturn


def get_tools(sVendorPath):
    '''
    Extract the tools for a vendor.

    Parameters:

      sVendor : (string)

    Returns: list of tool names
    '''
    lReturn = []
    lListing = os.listdir(sVendorPath)
    for sListing in lListing:
        if sListing.startswith('__'):
            continue
        if sListing == 'utils.py':
            continue
        if sListing.startswith('.'):
            continue
        lReturn.append(os.path.join(sVendorPath, remove_extension(sListing)))
    return lReturn


def remove_extension(sString):
    '''
    Removes the extension from a file name.

    Parameters:

      sString : (string)

    Returns: (string)
    '''
    return os.path.splitext(sString)[0]


def get_built_in_tool_module(lLogFile):
    '''
    Searches for a vendor tool in the that can parse the given logfile.

    Parameters:

      lLogFile : (list of strings)

    Returns:  (module)
    '''
    return get_tool_module(lLogFile, get_built_in_vendors)


def get_user_defined_tool_module(lLogFile):
    '''
    Searches for a vendor tool in the that can parse the given logfile.

    Parameters:

      lLogFile : (list of strings)

    Returns:  (module)
    '''
    return get_tool_module(lLogFile, get_user_defined_vendors)


def get_tool_module(lLogFile, fVendor):
    '''
    Searches for a vendor tool in the that can parse the given logfile.

    Parameters:

      lLogFile : (list of strings)
      fVendor  : function to search for vendors

    Returns:  (module)
    '''
    for sVendorPath in fVendor():
        for sToolPath in get_tools(sVendorPath):
            toolModule = import_vendor_module(sToolPath)
            if toolModule.is_logfile(lLogFile):
                return toolModule


def get_vendor_tool_module(lLogFile):
    '''
    Searches for a vendor tool that can parse the given logfile.

    Parameters:

      lLogFile : (list of strings)

    Returns:  (module)
    '''
    toolModule = get_built_in_tool_module(lLogFile)
    if toolModule is None:
        toolModule = get_user_defined_tool_module(lLogFile)
    return toolModule


def create_warning_list(lLogFile, sLogFileName):
    '''
    Creates a warning list object from the provided logfile.

    Parameters:

      lLogFile : (string)

    Returns:  (warning list object)
    '''
    mTool = get_built_in_tool_module(lLogFile)
    if mTool is None:
        mTool = get_user_defined_tool_module(lLogFile)
    if mTool is None:
        print('ERROR: File ' + sLogFileName + ' is not recognized as a supported logfile.')
        sys.exit(2)
    return mTool.extract_warnings(lLogFile)


def apply_suppression_rules_to_warnings(oWarnList, oSupList):
    for oWarning in oWarnList.get_warnings():
        for oSuppression in oSupList.get_suppressions():
            suppress_warning_with_rule(oWarning, oSuppression)


def suppress_warning_with_rule(oWarning, oSuppression):
    '''
    Suppresses a warning based on a suppression rule.

    Parameters:

        oWarning : (warning object)

        oSuppression : (suppression rule object)

    Returns: Nothing
    '''
    if check_for_match(oWarning, oSuppression):
        oSuppression.add_suppressed_warning(oWarning)
        oWarning.add_suppression_rule(oSuppression)
        if oSuppression.get_investigate():
            oWarning.set_investigate()


def check_for_match(oWarning, oSuppression):
    '''
    Compares the IDs and messages between a warning and a suppression rule.

    Parameters:

        oWarning : (warning object)

        oSuppression : (suppression rule object)

    Returns: Boolean
    '''
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
    if re.match(oSuppression.get_warning_id(), oWarning.get_id()):
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


def write_junit_file(sFilename, lFile):
    write_file(sFilename, lFile, 5)


def write_report_file(sFilename, lFile):
    write_file(sFilename, lFile, 4)


def write_file(sFilename, lFile, iExitCode):
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
        sys.exit(iExitCode)

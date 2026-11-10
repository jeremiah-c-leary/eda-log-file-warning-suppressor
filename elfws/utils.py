
import importlib
import importlib.util
import os
import re
import sys
import yaml

from . import suppression
from . import suppression_list
from .exit_code import ExitCode

NOT_SPECIFIED = '<None>'

# Parser modules which have already been imported, keyed by tool path.
dToolModuleCache = {}


def read_suppression_file(sFileName):
    '''
    Attempts to read the suppression file and return an list of rules.

    Parameters:

       sFileName : (String)

    Returns:  dictionary
    '''
    try:
        return value_or_default(load_yaml_file(sFileName), {})
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as e:
        exit_with_suppression_file_error(e)


def load_yaml_file(sFileName):
    with open(sFileName) as yaml_file:
        return yaml.safe_load(yaml_file)


def exit_with_suppression_file_error(oError):
    print(oError)
    sys.exit(ExitCode.SUPPRESSION_FILE_ERROR)


def create_suppression_list(dSuppression):
    '''
    Processes a given dictionary and returns a suppression list object.

    If any rule is malformed, every problem found is printed and the
    program exits with code 1 (suppression file error).

    Parameters:

        dSuppression : (dict)

    Returns:  suppression list object
    '''
    lErrors = []
    lRules = extract_rules_from_suppression_file(dSuppression, lErrors)
    exit_if_suppression_file_has_errors(lErrors)
    return build_suppression_list(lRules)


def extract_rules_from_suppression_file(dSuppression, lErrors):
    '''
    Extracts all suppression rules below the suppress key.

    Parameters:

        dSuppression : (dict)

        lErrors : (list of strings) problems found are appended to this list

    Returns: list of suppression rules
    '''
    if not is_mapping(dSuppression):
        lErrors.append('suppression file must contain a mapping with a "suppress" key')
        return []
    if not has_suppress_section(dSuppression):
        return []
    return search_for_suppression_rules(dSuppression['suppress'], ['suppress'], lErrors)


def build_suppression_list(lRules):
    '''
    Creates a suppression list object containing the given rules.

    Parameters:

        lRules : (list of suppression rules)

    Returns:  suppression list object
    '''
    oReturn = suppression_list.SuppressionList()
    for oRule in lRules:
        oReturn.add_suppression(oRule)
    return oReturn


def exit_if_suppression_file_has_errors(lErrors):
    '''
    Prints all suppression file errors and exits with code 1 if there are any.

    Parameters:

        lErrors : (list of strings)

    Returns: Nothing
    '''
    if not has_errors(lErrors):
        return
    print_suppression_file_errors(lErrors)
    sys.exit(ExitCode.SUPPRESSION_FILE_ERROR)


def print_suppression_file_errors(lErrors):
    for sError in lErrors:
        print('ERROR: Suppression file: ' + sError)


def search_for_suppression_rules(dSubDict, lPath=None, lErrors=None):
    '''
    This function traverses all keys in a dictionary searching for the key 'rules.'

    NOTE:  This is a recusive function.

    When the key 'rules' is found, extract_suppression_rules is called..
    The rules returned are added to a list which is passed to the calling function.

    Parameters:

        dSubDict : (dict)

        lPath : (list of strings) keys leading to dSubDict, used in error messages

        lErrors : (list of strings) problems found are appended to this list

    Returns: list of suppression rules
    '''
    lPath = value_or_default(lPath, [])
    lErrors = value_or_default(lErrors, [])
    if is_missing(dSubDict):
        return []
    if not is_mapping(dSubDict):
        add_error(lErrors, format_path(lPath), 'expected a group or "rules" key, found ' + repr(dSubDict))
        return []
    lReturn = []
    for sKey in list(dSubDict.keys()):
        lReturn.extend(search_key_for_suppression_rules(dSubDict, sKey, lPath, lErrors))
    return lReturn


def search_key_for_suppression_rules(dSubDict, sKey, lPath, lErrors):
    '''
    Extracts rules if the key is a rules key, otherwise searches the group below the key.

    Parameters:

        dSubDict : (dict)

        sKey : (string) key in dSubDict to search

        lPath : (list of strings) keys leading to dSubDict, used in error messages

        lErrors : (list of strings) problems found are appended to this list

    Returns: list of suppression rules
    '''
    if is_rules_key(sKey):
        return extract_suppression_rules(dSubDict[sKey], lPath + [sKey], lErrors)
    return search_for_suppression_rules(dSubDict[sKey], lPath + [str(sKey)], lErrors)


def extract_suppression_rules(dRules, lPath=None, lErrors=None):
    '''
    Processes a rule dictionary and return a list of suppression rules.

    Malformed rules are skipped and described in lErrors.

    Parameters:

        dRules : (dict)

        lPath : (list of strings) keys leading to dRules, used in error messages

        lErrors : (list of strings) problems found are appended to this list

    Returns: list of suppression rules
    '''
    lPath = value_or_default(lPath, ['rules'])
    lErrors = value_or_default(lErrors, [])
    if is_missing(dRules):
        return []
    if not is_mapping(dRules):
        add_error(lErrors, format_path(lPath), 'expected warning ids, found ' + repr(dRules))
        return []
    lReturn = []
    for sId in list(dRules.keys()):
        lReturn.extend(extract_rules_for_warning_id(sId, dRules[sId], lPath + [str(sId)], lErrors))
    return lReturn


def extract_rules_for_warning_id(sId, lRules, lPath, lErrors):
    '''
    Processes the list of rules for a single warning id.

    Parameters:

        sId : (string) warning id

        lRules : (list of dictionaries)

        lPath : (list of strings) keys leading to the warning id, used in error messages

        lErrors : (list of strings) problems found are appended to this list

    Returns: list of suppression rules
    '''
    sIdLocation = format_path(lPath)
    if not is_list(lRules):
        add_error(lErrors, sIdLocation, 'expected a list of rules, found ' + repr(lRules))
        return []
    lReturn = []
    for iIndex, dSup in enumerate(lRules):
        oSupRule = extract_rule(sId, dSup, format_rule_location(sIdLocation, iIndex), lErrors)
        if was_rule_extracted(oSupRule):
            lReturn.append(oSupRule)
    return lReturn


def extract_rule(sId, dSup, sLocation, lErrors):
    '''
    Creates a suppression rule if the rule definition is valid.

    Parameters:

        sId : (string) warning id

        dSup : (dict) rule definition

        sLocation : (string) location of the rule, used in error messages

        lErrors : (list of strings) problems found are appended to this list

    Returns: suppression rule or None if the rule is not valid
    '''
    if not validate_rule_structure(dSup, sLocation, lErrors):
        return None
    oSupRule = create_suppression_rule(sId, dSup)
    if not validate_rule_regular_expressions(oSupRule, sLocation, lErrors):
        return None
    return oSupRule


def validate_rule_structure(dSup, sLocation, lErrors):
    '''
    Checks a rule definition is a mapping with a msg key.

    Parameters:

        dSup : (dict) rule definition

        sLocation : (string) location of the rule, used in error messages

        lErrors : (list of strings) problems found are appended to this list

    Returns: (boolean) True if the rule is valid
    '''
    if not is_mapping(dSup):
        add_error(lErrors, sLocation, 'expected a rule with a "msg" key, found ' + repr(dSup))
        return False
    if not has_message(dSup):
        add_error(lErrors, sLocation, 'rule is missing the required "msg" key')
        return False
    return True


def create_suppression_rule(sId, dSup):
    '''
    Creates a suppression rule from a valid rule definition.

    Parameters:

        sId : (string) warning id

        dSup : (dict) rule definition

    Returns: suppression rule
    '''
    oSupRule = suppression.Suppression(str(sId), str(dSup['msg']))
    update_suppression_author(oSupRule, dSup)
    update_suppression_comment(oSupRule, dSup)
    update_suppression_investigate(oSupRule, dSup)
    update_suppression_options(oSupRule, dSup)
    return oSupRule


def validate_rule_regular_expressions(oSupRule, sLocation, lErrors):
    '''
    Checks the warning id and message of a rule compile as regular expressions.

    Parameters:

        oSupRule : (suppression rule object)

        sLocation : (string) location of the rule, used in error messages

        lErrors : (list of strings) problems found are appended to this list

    Returns: (boolean) True if both regular expressions are valid
    '''
    fIdValid = validate_regular_expression(oSupRule.get_warning_id(), 'warning id', sLocation, lErrors)
    fMessageValid = validate_regular_expression(oSupRule.get_message(), 'msg', sLocation, lErrors)
    return fIdValid and fMessageValid


def validate_regular_expression(sRegex, sField, sLocation, lErrors):
    '''
    Checks a regular expression compiles.

    Parameters:

        sRegex : (string)

        sField : (string) name of the rule field, used in error messages

        sLocation : (string) location of the rule, used in error messages

        lErrors : (list of strings) problems found are appended to this list

    Returns: (boolean) True if the regular expression is valid
    '''
    try:
        re.compile(sRegex)
    except re.error as e:
        add_error(lErrors, sLocation, 'invalid regular expression in ' + sField + ' ' + repr(sRegex) + ': ' + str(e))
        return False
    return True


def add_error(lErrors, sLocation, sMessage):
    lErrors.append(sLocation + ': ' + sMessage)


def format_path(lPath):
    '''
    Formats a list of keys as a location in the suppression file.

    Parameters:

        lPath : (list of strings)

    Returns: (string)
    '''
    return ' -> '.join(lPath)


def format_rule_location(sIdLocation, iIndex):
    return sIdLocation + '[' + str(iIndex) + ']'


def value_or_default(oValue, oDefault):
    if is_missing(oValue):
        return oDefault
    return oValue


def has_errors(lErrors):
    return len(lErrors) > 0


def has_suppress_section(dSuppression):
    return not is_missing(dSuppression.get('suppress'))


def has_message(dSup):
    return not is_missing(dSup.get('msg'))


def is_rules_key(sKey):
    return sKey == 'rules'


def was_rule_extracted(oSupRule):
    return not is_missing(oSupRule)


def is_missing(oValue):
    return oValue is None


def is_mapping(oValue):
    return isinstance(oValue, dict)


def is_list(oValue):
    return isinstance(oValue, list)


def update_suppression_author(oSupRule, dSup):
    oSupRule.author = dSup.get('author', NOT_SPECIFIED)


def update_suppression_comment(oSupRule, dSup):
    oSupRule.comment = dSup.get('comment', NOT_SPECIFIED)


def update_suppression_investigate(oSupRule, dSup):
    '''
    Updates the suppression rule based on the investigate key.

    Parameters:

        oSupRule : (suppression rule object)

        dSup : (dictionary)

    Returns: Nothing
    '''
    oSupRule.investigate = bool(dSup.get('investigate', False))


def update_suppression_options(oSupRule, dSup):
    '''
    Updates the suppression rule based on the option key.

    Parameters:

        oSupRule : (suppression rule object)

        dSup : (dictionary)

    Returns: Nothing
    '''
    oSupRule.set_options(value_or_default(dSup.get('options'), []))


def read_log_file(sFileName):
    '''
    Reads a log file and strips off line endings.

    Parameters:

      sFileName : (string)

    Bytes which are not valid UTF-8 are replaced rather than causing an
    error, as EDA tools frequently write other encodings.

    Exits with code 6 if the file cannot be read.

    Returns: (list of strings)
    '''
    try:
        return read_lines_without_line_endings(sFileName)
    except OSError as e:
        exit_with_log_file_error(sFileName, e)


def read_lines_without_line_endings(sFileName):
    lLines = []
    with open(sFileName, encoding='utf-8', errors='replace') as oFile:
        for sLine in oFile:
            lLines.append(sLine.rstrip())
    return lLines


def exit_with_log_file_error(sFileName, oError):
    print('ERROR: Could not read log file ' + sFileName + ' : ' + str(oError))
    sys.exit(ExitCode.LOG_FILE_READ_ERROR)


def import_vendor_module(sToolPath):
    '''
    Imports a module based on the path provided.

    For example:
       elfws/vendor/microsemi/designer.py

    Parameters:

      sToolPath   : (string)

    Returns : (module) or None if the module could not be imported
    '''
    sToolPath = os.path.abspath(sToolPath)
    if sToolPath in dToolModuleCache:
        return dToolModuleCache[sToolPath]

    sModuleName = 'elfws_parser_' + re.sub(r'\W', '_', sToolPath)
    try:
        spec = importlib.util.spec_from_file_location(sModuleName, sToolPath + '.py')
        tool = importlib.util.module_from_spec(spec)
        sys.modules[sModuleName] = tool
        spec.loader.exec_module(tool)
    except Exception as e:
        sys.modules.pop(sModuleName, None)
        print('WARNING: Could not load parser ' + sToolPath + '.py : ' + repr(e), file=sys.stderr)
        tool = None

    dToolModuleCache[sToolPath] = tool
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
    lListing = sorted(os.listdir(sVendorPath))
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
    lListing = sorted(os.listdir(sVendorPath))
    for sListing in lListing:
        if sListing.startswith('__'):
            continue
        if sListing == 'utils.py':
            continue
        if sListing.startswith('.'):
            continue
        if not sListing.endswith('.py'):
            continue
        if not os.path.isfile(os.path.join(sVendorPath, sListing)):
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
            if toolModule is None:
                continue
            if toolModule.is_logfile(lLogFile):
                return toolModule


def get_vendor_tool_module(lLogFile):
    '''
    Searches for a vendor tool that can parse the given logfile.

    Parameters:

      lLogFile : (list of strings)

    Returns:  (module)
    '''
    toolModule = get_user_defined_tool_module(lLogFile)
    if toolModule is None:
        toolModule = get_built_in_tool_module(lLogFile)
    return toolModule


def create_warning_list(lLogFile, sLogFileName):
    '''
    Creates a warning list object from the provided logfile.

    Parameters:

      lLogFile : (string)

    Returns:  (warning list object)
    '''
    mTool = get_vendor_tool_module(lLogFile)
    if mTool is None:
        print('ERROR: File ' + sLogFileName + ' is not recognized as a supported logfile.')
        sys.exit(ExitCode.NO_MATCHING_PARSER)
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
    return do_ids_match(oWarning, oSuppression) and do_messages_match(oWarning, oSuppression)


def do_ids_match(oWarning, oSuppression):
    '''
    Checks if the suppression ID matches the warning ID.

    Parameters:

      oWarning : (warning object)

      oSuppression : (suppression object)

    Returns: (boolean)
    '''
    if re.fullmatch(oSuppression.get_warning_id(), oWarning.get_id()):
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
    write_file(sFilename, lFile, ExitCode.JUNIT_FILE_WRITE_ERROR)


def write_report_file(sFilename, lFile):
    write_file(sFilename, lFile, ExitCode.REPORT_FILE_WRITE_ERROR)


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

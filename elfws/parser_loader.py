
import importlib
import importlib.util
import os
import re
import sys

from elfws.exit_code import ExitCode

# Parser modules which have already been imported, keyed by tool path.
dToolModuleCache = {}


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


import argparse
import os
import sys


def parse_command_line_arguments():
    '''
    Parses the command line arguments and returns them.
    '''
    top_parser = argparse.ArgumentParser(
        prog='elfws',
        description='''Suppresses Warnings in logfiles.'''
        )

    subparsers = top_parser.add_subparsers()

    build_suppress_subparser(subparsers, sys.argv)
    build_version_parser(subparsers)

    oArgs = top_parser.parse_args()

    return oArgs


def build_suppress_help_parser(oParser):
    sVendors = ', '.join(get_vendors())
    oParser.add_argument('vendor', help=sVendors)
    oParser.add_argument('tool', help='Vendor tool')
    add_file_arguments_to_parser(oParser)


def build_suppress_vendor_help_parser(oParser):
    build_suppress_help_parser(oParser)


def build_suppress_tool_help_parser(oParser, sVendor):
    sTools = ', '.join(get_tools(sVendor))
    oParser.add_argument('vendor', help=sVendor)
    oParser.add_argument('tool', help=sTools)
    add_file_arguments_to_parser(oParser)


def build_full_suppress_parser(oParser, argv):
    lVendors = get_vendors()
    sVendor = extract_vendor_from_args(argv)
    oParser.add_argument('vendor', help=lVendors[0])
    lTools = get_tools(sVendor)
    oParser.add_argument('tool', help=', '.join(lTools))
    add_file_arguments_to_parser(oParser)


def add_file_arguments_to_parser(oParser):
    oParser.add_argument('log_file', help='Log file which will be checked for warnings')
    oParser.add_argument('suppression_file', help='Suppression file')


def build_suppress_subparser(oSubparser, lArgv):
    parser = oSubparser.add_parser('suppress', help='Suppress warnings')

    if is_dash_h_present(lArgv):
        if len(lArgv) == 3:
            build_suppress_help_parser(parser)
        elif extract_vendor_from_args(lArgv) not in get_vendors():
            build_suppress_vendor_help_parser(parser)
        else:
            build_suppress_tool_help_parser(parser, extract_vendor_from_args(lArgv))
    else:
        if len(lArgv) == 1:
            build_suppress_help_parser(parser)
            sys.argv.append('-h')
        elif len(lArgv) == 2:
            build_suppress_help_parser(parser)
            if lArgv[1] == 'suppress':
                sys.argv.append('-h')
        elif lArgv[2] not in get_vendors():
            build_suppress_vendor_help_parser(parser)
            sys.argv.append('-h')
        elif len(lArgv) == 3:
            build_suppress_tool_help_parser(parser, extract_vendor_from_args(lArgv))
            sys.argv.append('-h')
        elif len(lArgv) == 4:
            build_full_suppress_parser(parser, lArgv)
            sys.argv.append('-h')
        elif len(lArgv) == 5:
            build_full_suppress_parser(parser, lArgv)
            sys.argv.append('-h')
        else:
            build_full_suppress_parser(parser, lArgv)
    parser.set_defaults(which='suppress')


def remove_help_argument(argv):
    lReturn = argv.copy()
    if '-h' in lReturn:
        lReturn.remove('-h')
    if '--help' in lReturn:
        lReturn.remove('--help')
    return lReturn


def extract_vendor_from_args(argv):
    lTemp = remove_help_argument(argv)
    try:
        return lTemp[2]
    except IndexError:
        return None


def build_version_parser(oSubparser):
    parser = oSubparser.add_parser('version', help='Displays ELFWS version information')

    parser.set_defaults(which='version')


def get_vendors():
    '''
    Extract the vendors from the vendor directory.
    
    Returns: List of directory names
    '''
    lReturn = []
    sVendorPath = os.path.join(os.path.dirname(__file__),'vendor')
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

    Returns: list of tools names
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
    return os.path.splitext(sString)[0]


def is_dash_h_present(sysargv):
    if '-h' in sysargv:
        return True
    if '--help' in sysargv:
        return True
    return False



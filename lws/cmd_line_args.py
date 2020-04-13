
import argparse
import os
import sys


def parse_command_line_arguments():
    '''
    Parses the command line arguments and returns them.
    '''
    top_parser = argparse.ArgumentParser(
        prog='lws',
        description='''Suppresses Warnings in logfiles.'''
        )

    subparsers = top_parser.add_subparsers()

    build_suppress_subparser(subparsers, sys.argv)
    build_version_parser(subparsers)

    print_help_if_no_command_line_options_given(top_parser)

    return top_parser.parse_args()


def is_dash_h_present(sysargv):
    if '-h' in sysargv:
        return True
    return False


def build_suppress_help_parser(oParser):
    sVendors = ', '.join(get_vendors())
    oParser.add_argument('vendor', help=sVendors)
    oParser.add_argument('tool', help='Vendor tool')
    add_file_arguments_to_parser(oParser)


def build_suppress_tool_help_parser(oParser, sVendor):
    sTools = ', '.join(get_tools(sVendor))
    oParser.add_argument('vendor', help=sVendor)
    oParser.add_argument('tool', help=sTools)
    add_file_arguments_to_parser(oParser)

def add_file_arguments_to_parser(oParser):
    oParser.add_argument('log_file', help='Log file which will be checked for warnings')
    oParser.add_argument('suppression_file', help='Suppression file')

#def build_suppress_microsemi_help_parser(oParser, argv):
#    oParser.add_argument('vendor', help='Microsemi')
#    oParser.add_argument('tool', help='Designer')
#    oParser.add_argument('suppression_file', help='Suppression file')
#    oParser.add_argument('log_file', help='Log file which will be checked for warnings')
#
#def build_suppress_mentor_graphics_help_parser(oParser, argv):
#    oParser.add_argument('vendor', help='Mentor_Graphics')
#    oParser.add_argument('tool', help='Precision')
#    oParser.add_argument('suppression_file', help='Suppression file')
#    oParser.add_argument('log_file', help='Log file which will be checked for warnings')


def build_suppress_subparser(oSubparser, argv):
    parser = oSubparser.add_parser('suppress', help='Suppress warnings')
    if len(sys.argv) == 2 or (len(sys.argv) == 3 and is_dash_h_present(sys.argv)):
        build_suppress_help_parser(parser)
    elif len(sys.argv) == 3 or (len(sys.argv) == 4 and is_dash_h_present(sys.argv)):
        build_suppress_tool_help_parser(parser, argv[2])
    elif len(sys.argv) > 3 and '-h' not in sys.argv:
        lVendors = get_vendors()
        if argv[2] in lVendors:
            parser.add_argument('vendor', choices=[argv[2]], help=lVendors[0])
            lTools = get_tools(argv[2])
            parser.add_argument('tool', choices=lTools, help=', '.join(lTools))
        add_file_arguments_to_parser(oParser)
    parser.set_defaults(which='suppress')



def build_version_parser(oSubparser):
    parser = oSubparser.add_parser('version', help='Displays LWS version information')

    parser.set_defaults(which='version')


def print_help_if_no_command_line_options_given(oParser):
    '''
    Will print the help output if no command line arguments were given.
    '''
    if len(sys.argv) == 1:
        oParser.print_help()
        sys.exit(1)


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

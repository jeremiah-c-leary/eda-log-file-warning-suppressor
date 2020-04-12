
import argparse
import importlib
import sys
import yaml

from . import subcommand
from . import version
from . import suppression
from . import suppression_list


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


def build_suppress_help_parser(oParser, argv):
    oParser.add_argument('vendor', help='Microsemi, Mentor_Graphics')
    oParser.add_argument('tool', help='Vendor tool')
    oParser.add_argument('suppression_file', help='Suppression file')
    oParser.add_argument('log_file', help='Log file which will be checked for warnings')

def build_suppress_microsemi_help_parser(oParser, argv):
    oParser.add_argument('vendor', help='Microsemi')
    oParser.add_argument('tool', help='Designer')
    oParser.add_argument('suppression_file', help='Suppression file')
    oParser.add_argument('log_file', help='Log file which will be checked for warnings')

def build_suppress_mentor_graphics_help_parser(oParser, argv):
    oParser.add_argument('vendor', help='Mentor_Graphics')
    oParser.add_argument('tool', help='Precision')
    oParser.add_argument('suppression_file', help='Suppression file')
    oParser.add_argument('log_file', help='Log file which will be checked for warnings')


def build_suppress_subparser(oSubparser, argv):
    parser = oSubparser.add_parser('suppress', help='Suppress warnings')
    if len(sys.argv) == 2 or (len(sys.argv) == 3 and is_dash_h_present(sys.argv)):
        build_suppress_help_parser(parser, argv)
    elif len(sys.argv) == 3 or (len(sys.argv) == 4 and is_dash_h_present(sys.argv)):
        if argv[2] == 'Microsemi':
            build_suppress_microsemi_help_parser(parser, argv)
        if argv[2] == 'Mentor_Graphics':
            build_suppress_mentor_graphics_help_parser(parser, argv)
    elif len(sys.argv) > 3 and '-h' not in sys.argv:
        if argv[2] == 'Microsemi':
            parser.add_argument('vendor', choices=['Microsemi'], help='Microsemi')
            parser.add_argument('tool', choices=['Designer'], help='Designer')
        if argv[2] == 'Mentor_Graphics':
            parser.add_argument('vendor', choices=['Mentor_Graphics'])
            parser.add_argument('tool', choices=['Precision', 'vsim'])
        parser.add_argument('suppression_file', help='Suppression file')
        parser.add_argument('log_file', help='Log file which will be checked for warnings')
    parser.set_defaults(which='suppress')


def build_vendor_subparser(oSubparser):

    parser = oSubparser.add_parser('Mentor_Graphics', help='Mentor Graphics EDA tools')
    parser.set_defaults(which='mentor_graphics')

    parser = oSubparser.add_parser('Microsemi', help='Microsemi EDA tools')
    parser.set_defaults(which='microsemi')


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


def main():
    '''
    Main routine of the Logfile Warning Suppressor (LWS) program.
    '''

    commandLineArguments = parse_command_line_arguments()

    if commandLineArguments.which == 'version':
        version.print_version()

    dSup = read_suppression_file(commandLineArguments.suppression_file)
    oSupList = create_suppression_list(dSup)

    lLogFile = read_log_file(commandLineArguments.log_file)
    toolModule = importlib.import_module('lws.vendor.' + commandLineArguments.vendor.lower() + '.' + commandLineArguments.tool.lower())
    oWarnList = toolModule.extract_warnings(lLogFile)

if __name__ == '__main__':
    main()

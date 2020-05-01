
import argparse
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

    build_create_subparser(subparsers)
    build_report_subparser(subparsers)
    build_show_subparser(subparsers)
    build_suppress_subparser(subparsers)
    build_version_parser(subparsers)

    oArgs = top_parser.parse_args()

    print_help_if_no_command_line_options_given(top_parser)

    return oArgs


def print_help_if_no_command_line_options_given(oParser):
    '''
    Will print the help output if no command line arguments were given.
    '''
    if len(sys.argv) == 1:
        oParser.print_help()
        sys.exit(1)


def add_file_arguments_to_parser(oParser):
    oParser.add_argument('log_file', help='Log file to check for warnings')
    oParser.add_argument('suppression_file', help='YAML formatted warning suppression file')


def build_create_subparser(oSubparser):
    parser = oSubparser.add_parser('create', help='Create suppression file')
    parser.add_argument('log_file', help='Log file with warnings to extract')
    parser.add_argument('output_suppression_file', help='Suppression file to create')
    parser.add_argument('--suppression_file', help='Existing suppression file to filter out existing')

    parser.set_defaults(which='create')


def build_report_subparser(oSubparser):
    parser = oSubparser.add_parser('report', help='Generate an audit report')
    add_file_arguments_to_parser(parser)
    parser.add_argument('report_file', help='Output report file')
    parser.add_argument('--junit', help='Generate JUnit XML file JUNIT')

    parser.set_defaults(which='report')


def build_suppress_subparser(oSubparser):
    parser = oSubparser.add_parser('suppress', help='Suppresses warnings in logfiles')
    add_file_arguments_to_parser(parser)

    parser.set_defaults(which='suppress')


def build_show_subparser(oSubparser):
    parser = oSubparser.add_parser('show', help='Show warnings in logfiles')
    parser.add_argument('log_file', help='Log file to show warnings')

    parser.set_defaults(which='show')


def build_version_parser(oSubparser):
    parser = oSubparser.add_parser('version', help='Displays ELFWS version information')

    parser.set_defaults(which='version')

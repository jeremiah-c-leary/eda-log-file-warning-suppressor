import sys

from . import cmd_line_args
from . import subcommand


def main():
    '''
    Main routine of the EDA Log File Warning Suppressor (ELFWS) program.
    '''

    commandLineArguments = cmd_line_args.parse_command_line_arguments()

    if commandLineArguments.which == 'version':
        subcommand.version.print_version()
    elif commandLineArguments.which == 'suppress':
        subcommand.suppress.suppress(commandLineArguments)
    elif commandLineArguments.which == 'show':
        subcommand.show.show(commandLineArguments)
    elif commandLineArguments.which == 'create':
        subcommand.create.create(commandLineArguments)
    elif commandLineArguments.which == 'report':
        subcommand.report.report(commandLineArguments)

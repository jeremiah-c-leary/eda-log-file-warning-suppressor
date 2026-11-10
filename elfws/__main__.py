import sys

from . import cmd_line_args
from . import error


def main():
    '''
    Main routine of the EDA Log File Warning Suppressor (ELFWS) program.
    '''
    iExitCode = run_and_report_errors()
    sys.exit(iExitCode)


def run_and_report_errors():
    try:
        return run()
    except error.ElfwsError as oError:
        return report_error(oError)


def run():
    oCommandLineArguments = cmd_line_args.parse_command_line_arguments()
    return oCommandLineArguments.run_subcommand(oCommandLineArguments)


def report_error(oError):
    if has_message(oError):
        print(str(oError))
    return oError.iExitCode


def has_message(oError):
    return str(oError) != ''


if __name__ == '__main__':
    main()

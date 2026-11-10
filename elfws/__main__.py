from . import cmd_line_args
from . import subcommand


def main():
    '''
    Main routine of the EDA Log File Warning Suppressor (ELFWS) program.
    '''

    oCommandLineArguments = cmd_line_args.parse_command_line_arguments()

    if oCommandLineArguments.which == 'version':
        subcommand.version.print_version()
    elif oCommandLineArguments.which == 'suppress':
        subcommand.suppress.suppress(oCommandLineArguments)
    elif oCommandLineArguments.which == 'show':
        subcommand.show.show(oCommandLineArguments)
    elif oCommandLineArguments.which == 'create':
        subcommand.create.create(oCommandLineArguments)
    elif oCommandLineArguments.which == 'report':
        subcommand.report.report(oCommandLineArguments)


if __name__ == '__main__':
    main()

from . import cmd_line_args


def main():
    '''
    Main routine of the EDA Log File Warning Suppressor (ELFWS) program.
    '''

    oCommandLineArguments = cmd_line_args.parse_command_line_arguments()
    oCommandLineArguments.run_subcommand(oCommandLineArguments)


if __name__ == '__main__':
    main()

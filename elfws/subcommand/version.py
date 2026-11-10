
from elfws import version as version_number
from elfws.exit_code import ExitCode


def print_version(oCommandLineArguments):

    print('EDA Log File Warning Suppressor (ELFWS) version ' + version_number.version)
    return ExitCode.SUCCESS

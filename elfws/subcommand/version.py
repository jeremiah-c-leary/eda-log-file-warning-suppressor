
import sys

from elfws import version as version_number
from elfws.exit_code import ExitCode


def version(oCommandLineArguments):
    print_version()


def print_version():

    print('EDA Log File Warning Suppressor (ELFWS) version ' + version_number.version)
    sys.exit(ExitCode.SUCCESS)

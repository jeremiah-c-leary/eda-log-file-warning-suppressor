
import sys

from elfws import version
from elfws.exit_code import ExitCode


def print_version():

    print('EDA Log File Warning Suppressor (ELFWS) version ' + version.version)
    sys.exit(ExitCode.SUCCESS)

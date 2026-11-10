
import sys

from elfws import display
from elfws.report import junit
from elfws import suppression_list
from elfws import utils
from elfws.exit_code import ExitCode


def show(oCommandLineArguments):

    oSupList = suppression_list.SuppressionList()
    oWarnList = utils.read_warning_list(oCommandLineArguments.log_file)

    display.results(oCommandLineArguments.log_file, utils.NOT_SPECIFIED, oSupList, oWarnList)
    junit.write_junit_file_if_requested(oCommandLineArguments.junit, oWarnList, oSupList)

    sys.exit(ExitCode.SUCCESS)

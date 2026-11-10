
import sys

from elfws import display
from elfws.report import junit
from elfws import suppression_list
from elfws import log_file
from elfws import suppression_file
from elfws.exit_code import ExitCode


def show(oCommandLineArguments):

    oSupList = suppression_list.SuppressionList()
    oWarnList = log_file.read_warning_list(oCommandLineArguments.log_file)

    display.results(oCommandLineArguments.log_file, suppression_file.NOT_SPECIFIED, oSupList, oWarnList)
    junit.write_junit_file_if_requested(oCommandLineArguments.junit, oWarnList, oSupList)

    sys.exit(ExitCode.SUCCESS)

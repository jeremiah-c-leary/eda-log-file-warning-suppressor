
import sys

from elfws import display
from elfws import junit_results
from elfws import suppression_results
from elfws.exit_code import ExitCode


def show(oCommandLineArguments):

    oResults = suppression_results.create_results_without_suppression_file(oCommandLineArguments.log_file)

    display.print_results(oResults)
    junit_results.write_junit_file_if_requested(oCommandLineArguments.junit, oResults)

    sys.exit(ExitCode.SUCCESS)

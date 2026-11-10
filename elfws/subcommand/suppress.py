
from elfws import display
from elfws import suppression_results
from elfws.exit_code import ExitCode


def suppress(oCommandLineArguments):

    oResults = suppression_results.apply_suppression_file(oCommandLineArguments.log_file, oCommandLineArguments.suppression_file)

    display.print_results(oResults)

    return ExitCode.SUCCESS

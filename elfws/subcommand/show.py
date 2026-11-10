
import sys

from elfws import display
from elfws.report import junit
from elfws import suppression_list
from elfws import utils
from elfws.exit_code import ExitCode


def show(oCommandLineArguments):

    oSupList = suppression_list.SuppressionList()

    lLogFile = utils.read_log_file(oCommandLineArguments.log_file)

    oWarnList = utils.create_warning_list(lLogFile, oCommandLineArguments.log_file)

    display.results(oCommandLineArguments.log_file, '<None>', oSupList, oWarnList)

    if oCommandLineArguments.junit:
        lJUnitFile = junit.generate_junit_xml_file(oCommandLineArguments, oWarnList, oSupList)
        utils.write_junit_file(oCommandLineArguments.junit, lJUnitFile)

    sys.exit(ExitCode.SUCCESS)


import sys

from elfws import log_file
from elfws import output_file
from elfws import rule_matching
from elfws import suppression_file
from elfws import display
from elfws.report import junit
from elfws.exit_code import ExitCode


def report(oCommandLineArguments):
    oSupList = suppression_file.read_suppression_list(oCommandLineArguments.suppression_file)
    oWarnList = log_file.read_warning_list(oCommandLineArguments.log_file)
    rule_matching.apply_suppression_rules_to_warnings(oWarnList, oSupList)

    lReport = build_report(oCommandLineArguments.log_file, oCommandLineArguments.suppression_file, oWarnList, oSupList)
    output_file.write_report_file(oCommandLineArguments.report_file, lReport)
    junit.write_junit_file_if_requested(oCommandLineArguments.junit, oWarnList, oSupList)

    sys.exit(ExitCode.SUCCESS)


def build_report(sLogFileName, sSuppressionFileName, oWarnList, oSupList):
    lReport = []
    lReport.extend(build_header(sLogFileName, sSuppressionFileName))
    lReport.extend(build_unsuppressed_warnings_section(oWarnList))
    lReport.extend(build_suppressed_warnings_section(oSupList))
    lReport.extend(build_unused_suppression_rules_section(oSupList))
    lReport.extend(build_warnings_under_investigation_section(oSupList))
    lReport.extend(build_multiply_suppressed_warnings_section(oWarnList))
    lReport.extend(build_summary_section(oWarnList, oSupList))
    return lReport


def build_header(sLogFileName, sSuppressionFileName):
    lReturn = []
    lReturn.extend(display.build_header(sLogFileName, sSuppressionFileName))
    lReturn.extend(display.build_table_of_contents())
    return lReturn


def build_unsuppressed_warnings_section(oWarnList):
    lReturn = []
    lReturn.extend(display.build_report_section_divider(' 1. Unsuppressed Warnings'))
    lReturn.extend(display.build_warning_table(oWarnList.get_unsuppressed_warnings(), 2))
    return lReturn


def build_suppressed_warnings_section(oSupList):
    lReturn = []
    lReturn.extend(display.build_report_section_divider(' 2. Suppressed Warnings'))
    for oSup in oSupList.get_suppressions_which_suppressed_a_warning():
        lReturn.extend(display.build_suppressed_warning_header(oSup, 2))
        lReturn.extend(display.build_suppressed_warning_table(oSup, 4))
    return lReturn


def build_unused_suppression_rules_section(oSupList):
    lReturn = []
    lReturn.extend(display.build_report_section_divider(' 3. Unused Suppression Rules'))
    for oSup in oSupList.get_suppressions_which_did_not_suppress_a_warning():
        lReturn.extend(display.build_suppression_item(oSup, 2))
    return lReturn


def build_warnings_under_investigation_section(oSupList):
    lReturn = []
    lReturn.extend(display.build_report_section_divider(' 4. Warnings Under Investigation'))
    for oSup in oSupList.get_investigate_suppression_rules():
        lReturn.extend(display.build_suppressed_warning_header(oSup, 2))
        lReturn.extend(display.build_suppressed_warning_table(oSup, 4))
    return lReturn


def build_multiply_suppressed_warnings_section(oWarnList):
    lReturn = []
    lReturn.extend(display.build_report_section_divider(' 5. Warnings Suppressed by Multiple Rules'))
    for oWarn in oWarnList.get_warnings_suppressed_by_multiple_rules():
        lReturn.extend(display.build_multiply_suppressed_warning_header(oWarn, 2))
        for oSup in oWarn.get_suppressed_by_rules():
            lReturn.extend(display.build_suppression_item(oSup, 4))
    return lReturn


def build_summary_section(oWarnList, oSupList):
    lReturn = []
    lReturn.extend(display.build_report_section_divider(' 6. Summary'))
    lReturn.extend(display.build_report_summary_section(oWarnList, oSupList))
    return lReturn

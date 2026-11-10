
import sys

from elfws import display
from elfws import junit_results
from elfws import output_file
from elfws import suppression_results
from elfws.exit_code import ExitCode


def report(oCommandLineArguments):
    oResults = suppression_results.apply_suppression_file(oCommandLineArguments.log_file, oCommandLineArguments.suppression_file)

    lReport = build_report(oResults)
    output_file.write_report_file(oCommandLineArguments.report_file, lReport)
    junit_results.write_junit_file_if_requested(oCommandLineArguments.junit, oResults)

    sys.exit(ExitCode.SUCCESS)


def build_report(oResults):
    lReport = []
    lReport.extend(build_header(oResults))
    lReport.extend(build_unsuppressed_warnings_section(oResults.oWarnList))
    lReport.extend(build_suppressed_warnings_section(oResults.oSupList))
    lReport.extend(build_unused_suppression_rules_section(oResults.oSupList))
    lReport.extend(build_warnings_under_investigation_section(oResults.oSupList))
    lReport.extend(build_multiply_suppressed_warnings_section(oResults.oWarnList))
    lReport.extend(build_summary_section(oResults))
    return lReport


def build_header(oResults):
    lReturn = []
    lReturn.extend(display.build_header(oResults.sLogFileName, oResults.sSuppressionFileName))
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


def build_summary_section(oResults):
    lReturn = []
    lReturn.extend(display.build_report_section_divider(' 6. Summary'))
    lReturn.extend(display.build_report_summary_section(oResults))
    return lReturn

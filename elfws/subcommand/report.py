
import re
import sys

from elfws import warning_list
from elfws import utils
from elfws import display
from elfws.report import junit


def report(cla):

    dSup = utils.read_suppression_file(cla.suppression_file)
    oSupList = utils.create_suppression_list(dSup)

    lLogFile = utils.read_log_file(cla.log_file)

    oWarnList = utils.create_warning_list(lLogFile, cla.log_file)

    utils.apply_suppression_rules_to_warnings(oWarnList, oSupList)

    lReport = []
    build_header(cla, lReport)
    build_section_1(oWarnList, lReport)
    build_section_2(oSupList, lReport)
    build_section_3(oSupList, lReport)
    build_section_4(oSupList, lReport)
    build_section_5(oWarnList, lReport)
    build_summary(oWarnList, oSupList, lReport)

    utils.write_file(cla.report_file, lReport)

    if cla.junit:
        lJUnitFile = junit.generate_junit_xml_file(cla, oWarnList, oSupList)
        utils.write_file(cla.junit, lJUnitFile)


def build_header(cla, lReport):
    lReport.extend(display.build_header(cla.log_file, cla.suppression_file))
    lReport.extend(display.build_table_of_contents())


def build_section_1(oWarnList, lReport):
    lNonSuppressWarnings = oWarnList.get_unsuppressed_warnings()
    lReport.extend(display.build_report_section_divider(' 1. Unsuppressed Warnings'))
    lReport.extend(display.build_warning_table(lNonSuppressWarnings, 2))


def build_section_2(oSupList, lReport):
    lReport.extend(display.build_report_section_divider(' 2. Suppressed Warnings'))
    for oSup in oSupList.get_suppressions_which_suppressed_a_warning():
        lReport.extend(display.build_suppressed_warning_header(oSup, 2))
        lReport.extend(display.build_suppressed_warning_table(oSup, 4))


def build_section_3(oSupList, lReport):
    lReport.extend(display.build_report_section_divider(' 3. Unused Suppression Rules'))
    for oSup in oSupList.get_suppressions_which_did_not_suppress_a_warning():
        lReport.extend(display.build_suppression_item(oSup, 2))


def build_section_4(oSupList, lReport):
    lReport.extend(display.build_report_section_divider(' 4. Warnings Under Investigation'))
    for oSup in oSupList.get_investigate_suppression_rules():
        lReport.extend(display.build_suppressed_warning_header(oSup, 2))
        lReport.extend(display.build_suppressed_warning_table(oSup, 4))


def build_section_5(oWarnList, lReport):
    lReport.extend(display.build_report_section_divider(' 5. Warnings Suppressed by Multiple Rules'))
    for oWarn in oWarnList.get_warnings_suppressed_by_multiple_rules():
        lReport.extend(display.build_multiply_suppressed_warning_header(oWarn, 2))
        for oSup in oWarn.get_suppressed_by_rules():
            lReport.extend(display.build_suppression_item(oSup, 4))


def build_summary(oWarnList, oSupList, lReport):
    lReport.extend(display.build_report_section_divider(' 6. Summary'))
    lReport.extend(display.build_report_summary_section(oWarnList, oSupList))

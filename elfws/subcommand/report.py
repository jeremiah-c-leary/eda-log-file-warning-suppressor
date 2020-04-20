
import re
import sys

from elfws import warning_list
from elfws import utils
from elfws import display


def report(cla):

    dSup = utils.read_suppression_file(cla.suppression_file)
    oSupList = utils.create_suppression_list(dSup)

    lLogFile = utils.read_log_file(cla.log_file)

    oWarnList = utils.create_warning_list(lLogFile, cla.log_file)

    oNonSuppressWarnings = extract_non_suppressed_warnings(oWarnList, oSupList)

    lReport = []
    lReport.extend(display.build_header(cla.log_file, cla.suppression_file))
    lReport.extend(display.build_table_of_contents())
    lReport.extend(display.build_report_section_divider(' 1. Unsuppressed Warnings'))
    lReport.extend(display.build_warning_table(oNonSuppressWarnings, 2))
    lReport.extend(display.build_report_section_divider(' 2. Suppressed Warnings'))
    for oSup in oSupList.get_suppressions_which_suppressed_a_warning():
        lReport.extend(display.build_suppressed_warning_header(oSup, 2))
        lReport.extend(display.build_suppressed_warning_table(oSup, 4))
    lReport.extend(display.build_report_section_divider(' 3. Unused Suppression Rules'))
    for oSup in oSupList.get_suppressions_which_did_not_suppress_a_warning():
        lReport.extend(display.build_suppression_item(oSup, 2))
    lReport.extend(display.build_report_section_divider(' 4. Warnings Suppressed by Multiple Rules'))
    for oWarn in oWarnList.get_warnings_suppressed_by_multiple_rules():
        lReport.extend(display.build_multiply_suppressed_warning_header(oWarn, 2))
        for oSup in oWarn.get_suppressed_by_rules():
            lReport.extend(display.build_suppression_item(oSup, 4))
    lReport.extend(display.build_report_summary_section(oWarnList, oSupList))


    for sLine in lReport:
        print(sLine)


def extract_non_suppressed_warnings(oWarnList, oSupList):
    oReturn = warning_list.create()
    for oWarning in oWarnList.get_warnings():
        fMatchFound = False
        for oSuppression in oSupList.get_suppressions():
            fMatchFound = check_for_match(oWarning, oSuppression)
            if fMatchFound:
                oSuppression.add_suppressed_warning(oWarning)
                oWarning.add_suppression_rule(oSuppression)
        if not fMatchFound:
            oReturn.add_warning(oWarning)

    return oReturn


def check_for_match(oWarning, oSuppression):
    if do_ids_match(oWarning, oSuppression):
        return do_messages_match(oWarning, oSuppression)
    return False


def do_ids_match(oWarning, oSuppression):
    '''
    Checks if the suppression ID matches the warning ID.

    Parameters:

      oWarning : (warning object)

      oSuppression : (suppression object)

    Returns: (boolean)
    '''
    if oWarning.get_id() == oSuppression.get_warning_id():
        return True
    return False


def do_messages_match(oWarning, oSuppression):
    '''
    Checks if the suppression message matches the warning message.

    Parameters:

      oWarning : (warning object)

      oSuppression : (suppression object)

    Returns: (boolean)
    '''
    if re.match('^.*' + oSuppression.get_message(), oWarning.get_message()):
        return True
    return False

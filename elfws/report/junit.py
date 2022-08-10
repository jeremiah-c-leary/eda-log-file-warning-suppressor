
from elfws import junit


def generate_junit_xml_file(cla, oWarnList, oSupList):
    '''
    Generates a JUnit XML file.

    Parameters:

      cla : (command line arguments)

      oWarnList : (warning_list object)

      oSupList : (suppression_list object)

    Returns: Nothing
    '''
    oXmlFile = junit.xmlfile()
    oTestsuite = junit.testsuite('eda-log-file-warning-suppressor', str(0))

    oTestsuite.add_testcase(build_junit_unsuppressed_testcase(oWarnList))
    oTestsuite.add_testcase(build_junit_unused_suppression_rule_testcase(oSupList))
    oTestsuite.add_testcase(build_junit_multiply_suppressed_warnings_testcase(oWarnList))

    oXmlFile.add_testsuite(oTestsuite)
    return oXmlFile.build_junit()


def build_junit_unsuppressed_testcase(oWarnList):
    return build_junit_warning_testcase(oWarnList.get_unsuppressed_warnings(), 'Unsuppressed Warnings')


def build_junit_unused_suppression_rule_testcase(oSupList):
    oTestcase = junit.testcase('Unused Suppression Rules', str(0), 'failure')
    lSuppressions = oSupList.get_suppressions_which_did_not_suppress_a_warning()
    if len(lSuppressions) > 0:
        oFailure = junit.failure('Failure')
        for oSup in lSuppressions:
            sOutput = '[' + ']['.join([oSup.get_warning_id(), str(oSup.get_author()), oSup.get_message(), oSup.get_comment()]) + ']'
            oFailure.add_text(sOutput)
        oTestcase.add_failure(oFailure)
    return oTestcase


def build_junit_multiply_suppressed_warnings_testcase(oWarnList):
    return build_junit_warning_testcase(oWarnList.get_warnings_suppressed_by_multiple_rules(), 'Multiply Suppressed Warnings')


def build_junit_warning_testcase(lWarnings, sTestCaseName):
    oTestcase = junit.testcase(sTestCaseName, str(0), 'failure')

    if len(lWarnings) > 0:
        oFailure = junit.failure('Failure')
        for oWarning in lWarnings:
            oFailure.add_text(construct_junit_warning_output(oWarning))
        oTestcase.add_failure(oFailure)
    return oTestcase


def construct_junit_warning_output(oWarning):
    return '[' + oWarning.get_id() + '][' + str(oWarning.get_linenumber()) + ']:' + oWarning.get_message()

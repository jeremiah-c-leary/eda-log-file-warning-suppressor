
from elfws import junit
from elfws import output_file


def write_junit_file_if_requested(sJUnitFileName, oResults):
    '''
    Writes a JUnit XML file if a file name was given on the command line.

    Parameters:

      sJUnitFileName : (string) None when no JUnit file was requested

      oResults : (SuppressionResults object)

    Returns: Nothing
    '''
    if not is_junit_file_requested(sJUnitFileName):
        return
    lJUnitFile = generate_junit_xml_file(oResults)
    output_file.write_junit_file(sJUnitFileName, lJUnitFile)


def is_junit_file_requested(sJUnitFileName):
    return sJUnitFileName is not None


def generate_junit_xml_file(oResults):
    '''
    Generates a JUnit XML file.

    Parameters:

      oResults : (SuppressionResults object)

    Returns: (list of strings)
    '''
    oXmlFile = junit.XmlFile()
    oTestsuite = junit.TestSuite('eda-log-file-warning-suppressor', str(0))

    oTestsuite.add_testcase(build_junit_unsuppressed_testcase(oResults.oWarnList))
    oTestsuite.add_testcase(build_junit_unused_suppression_rule_testcase(oResults.oSupList))
    oTestsuite.add_testcase(build_junit_multiply_suppressed_warnings_testcase(oResults.oWarnList))

    oXmlFile.add_testsuite(oTestsuite)
    return oXmlFile.build_junit()


def build_junit_unsuppressed_testcase(oWarnList):
    return build_junit_warning_testcase(oWarnList.get_unsuppressed_warnings(), 'Unsuppressed Warnings')


def build_junit_unused_suppression_rule_testcase(oSupList):
    oTestcase = junit.TestCase('Unused Suppression Rules', str(0), 'failure')
    lSuppressions = oSupList.get_suppressions_which_did_not_suppress_a_warning()
    lSuppressions = remove_suppressions_per_options(lSuppressions)
    if len(lSuppressions) > 0:
        oFailure = junit.Failure('Failure')
        for oSup in lSuppressions:
            sOutput = '[' + ']['.join([oSup.get_warning_id(), str(oSup.get_author()), oSup.get_message(), oSup.get_comment()]) + ']'
            oFailure.add_text(sOutput)
        oTestcase.add_failure(oFailure)
    return oTestcase


def build_junit_multiply_suppressed_warnings_testcase(oWarnList):
    return build_junit_warning_testcase(oWarnList.get_warnings_suppressed_by_multiple_rules(), 'Multiply Suppressed Warnings')


def build_junit_warning_testcase(lWarnings, sTestCaseName):
    oTestcase = junit.TestCase(sTestCaseName, str(0), 'failure')

    if len(lWarnings) > 0:
        oFailure = junit.Failure('Failure')
        for oWarning in lWarnings:
            oFailure.add_text(construct_junit_warning_output(oWarning))
        oTestcase.add_failure(oFailure)
    return oTestcase


def construct_junit_warning_output(oWarning):
    return '[' + oWarning.get_id() + '][' + str(oWarning.get_linenumber()) + ']:' + oWarning.get_message()


def remove_suppressions_per_options(lSuppressions):
    lReturn = []
    for oSuppression in lSuppressions:
        if not oSuppression.has_option('suppress_in_json_if_unmatched'):
            lReturn.append(oSuppression)
    return lReturn

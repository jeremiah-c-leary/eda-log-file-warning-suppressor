
import unittest

from elfws import suppression
from elfws import suppression_list
from elfws import suppression_results
from elfws import warning
from elfws import warning_list


sLogFile = 'tests/vendor/microsemi/designer/warning_messages.log'
sSuppressionFile = 'tests/subcommand/report/suppress_microsemi_designer_logfile.yaml'


class test_suppression_results(unittest.TestCase):

    def test_apply_suppression_rules(self):
        oWarnList = warning_list.WarningList()
        oWarnList.add_warning(warning.LogWarning('A', 'port unused'))
        oWarnList.add_warning(warning.LogWarning('B', 'latch inferred'))
        oSupList = suppression_list.SuppressionList()
        oSupList.add_suppression(suppression.Suppression('A', 'unused'))

        oResults = suppression_results.SuppressionResults('log', oWarnList, 'sup', oSupList)
        oResults.apply_suppression_rules()

        self.assertEqual(['B'], [o.get_id() for o in oResults.oWarnList.get_unsuppressed_warnings()])
        self.assertEqual(['A'], [o.get_id() for o in oSupList.get_suppressions()[0].get_suppressed_warnings()])

    def test_apply_suppression_file(self):
        oResults = suppression_results.apply_suppression_file(sLogFile, sSuppressionFile)

        self.assertEqual(sLogFile, oResults.sLogFileName)
        self.assertEqual(sSuppressionFile, oResults.sSuppressionFileName)
        self.assertEqual(5, oResults.oWarnList.get_number_of_warnings())
        self.assertEqual(1, len(oResults.oWarnList.get_unsuppressed_warnings()))

    def test_create_results_without_suppression_file(self):
        oResults = suppression_results.create_results_without_suppression_file(sLogFile)

        self.assertEqual('<None>', oResults.sSuppressionFileName)
        self.assertEqual(0, oResults.oSupList.get_number_of_suppressions())
        self.assertEqual(5, len(oResults.oWarnList.get_unsuppressed_warnings()))


import datetime
import os
import sys
import unittest
from unittest import mock

from elfws import __main__
from elfws import version
from elfws import utils

sWarningFile = 'tests/vendor/microsemi/designer/warning_messages.log'
sSupFile = 'tests/subcommand/suppress/suppress_microsemi_designer_logfile.yaml'

sYamlFile = 'deleteme.yaml'
sReportFile = 'deleteme.rpt'
sXmlFile = 'deleteme.xml'

class test_arguments(unittest.TestCase):

    @mock.patch('elfws.version.version', '0.1')
    @mock.patch('elfws.display.datetime')
    def test_report_w_junit_output(self, mock_datetime):
        mock_datetime.now.return_value = 'Some Date'
        sys.argv = ['elfws', 'report', 'tests/option/suppress_in_json_if_unmatched/warning_messages.log', 'tests/option/suppress_in_json_if_unmatched/suppression.yaml', sReportFile, '--junit', sXmlFile]
        __main__.main()

        lExpected = utils.read_log_file('tests/option/suppress_in_json_if_unmatched/expected.xml')
        lActual = utils.read_log_file(sXmlFile)

        self.assertEqual(len(lExpected), len(lActual))
        for iIndex, sLine in enumerate(lExpected):
            if not iIndex == 1:
                self.assertEqual(sLine, lActual[iIndex])

        lExpected = utils.read_log_file('tests/option/suppress_in_json_if_unmatched/expected.rpt')
        lActual = utils.read_log_file(sReportFile)

        self.assertEqual(len(lExpected), len(lActual))
        self.assertEqual(lExpected, lActual)

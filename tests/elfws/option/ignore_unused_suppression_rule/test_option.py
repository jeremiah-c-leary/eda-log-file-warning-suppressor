
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

    def test_report_w_junit_output(self):
        sys.argv = ['elfws', 'report', 'tests/elfws/option/ignore_unused_suppression_rule/warning_messages.log', 'tests/elfws/option/ignore_unused_suppression_rule/suppression.yaml', sReportFile, '--junit', sXmlFile]
        __main__.main()

        lExpected = utils.read_log_file('tests/elfws/option/ignore_unused_suppression_rule/junit_output.xml')
        lActual = utils.read_log_file(sXmlFile)

        self.assertEqual(len(lExpected), len(lActual))
        for iIndex, sLine in enumerate(lExpected):
            if not iIndex == 1:
                self.assertEqual(sLine, lActual[iIndex])


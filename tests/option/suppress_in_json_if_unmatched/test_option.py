
import os
import unittest
from unittest import mock

from elfws import __main__
from elfws import log_file

sYamlFile = 'deleteme.yaml'
sReportFile = 'deleteme.rpt'
sXmlFile = 'deleteme.xml'

class test_arguments(unittest.TestCase):

    def setUp(self):
        if os.path.isfile(sYamlFile):
            os.remove(sYamlFile)
        if os.path.isfile(sReportFile):
            os.remove(sReportFile)
        if os.path.isfile(sXmlFile):
            os.remove(sXmlFile)
    
    def tearDown(self):
        if os.path.isfile(sYamlFile):
            os.remove(sYamlFile)
        if os.path.isfile(sReportFile):
            os.remove(sReportFile)
        if os.path.isfile(sXmlFile):
            os.remove(sXmlFile)

    @mock.patch('sys.argv', ['elfws', 'report', os.path.join(os.path.dirname(__file__), 'warning_messages.rpt'), os.path.join(os.path.dirname(__file__), 'suppression.yaml'), sReportFile, '--junit', sXmlFile])
    @mock.patch('elfws.version.version', '0.1')
    @mock.patch('elfws.display.datetime')
    def test_report_w_junit_output(self, mock_datetime):
        mock_datetime.now.return_value = 'Some Date'

        with self.assertRaises(SystemExit) as oContext:
            __main__.main()

        self.assertEqual(oContext.exception.code, 0)

        lExpected = log_file.read_log_file('tests/option/suppress_in_json_if_unmatched/expected.xml')
        lActual = log_file.read_log_file(sXmlFile)

        self.assertEqual(len(lExpected), len(lActual))
        for iIndex, sLine in enumerate(lExpected):
            if iIndex == 1:
                continue
            self.assertEqual(sLine, lActual[iIndex])

        lExpected = log_file.read_log_file('tests/option/suppress_in_json_if_unmatched/expected.rpt')
        lActual = log_file.read_log_file(sReportFile)

        self.assertEqual(len(lExpected), len(lActual))
        for iIndex, sLine in enumerate(lExpected):
            if iIndex == 3 or iIndex == 4:
                continue
            self.assertEqual(sLine, lActual[iIndex])

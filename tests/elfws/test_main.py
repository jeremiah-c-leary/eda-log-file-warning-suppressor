
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

class test_arguments(unittest.TestCase):

    def setUp(self):
        if os.path.isfile(sYamlFile):
            os.remove(sYamlFile)
        if os.path.isfile(sReportFile):
            os.remove(sReportFile)
    
    def tearDown(self):
        if os.path.isfile(sYamlFile):
            os.remove(sYamlFile)
        if os.path.isfile(sReportFile):
            os.remove(sReportFile)

    @mock.patch('sys.stdout')
    def test_version(self, mockStdout):
        sys.argv = ['elfws', 'version']
        try:
            __main__.main()
        except SystemExit:
            pass

        mockStdout.write.assert_has_calls([
            mock.call('EDA Log File Warning Suppressor (ELFWS) version ' + version.version), mock.call('\n')
        ])

    @mock.patch('elfws.version.version', '0.1')
    @mock.patch('sys.stdout')
    @mock.patch('elfws.display.datetime')
    def test_show(self, mock_datetime, mock_stdout):
        mock_datetime.now.return_value = 'Some Date'
        sys.argv = ['elfws', 'show', sWarningFile]
        __main__.main()

        lLogFile = utils.read_log_file('tests/elfws/show_output.txt')
        
        lExpected = []
        for sLine in lLogFile:
            lExpected.append(mock.call(sLine))
            lExpected.append(mock.call('\n'))

        mock_stdout.write.assert_has_calls(lExpected)

    @mock.patch('elfws.version.version', '0.1')
    def test_create_without_suppression_file(self):
        sys.argv = ['elfws', 'create', sWarningFile, sYamlFile]
        __main__.main()

        lExpected = utils.read_log_file('tests/elfws/create_yaml_wo_suppression.yaml')
        lActual = utils.read_log_file(sYamlFile)

        self.assertEqual(lExpected, lActual)

    @mock.patch('elfws.version.version', '0.1')
    def test_create_with_suppression_file(self):
        sys.argv = ['elfws', 'create', sWarningFile, sYamlFile, '--suppression_file', sSupFile]
        __main__.main()

        lExpected = utils.read_log_file('tests/elfws/create_yaml_with_suppression.yaml')
        lActual = utils.read_log_file(sYamlFile)

        self.assertEqual(lExpected, lActual)

    @mock.patch('elfws.version.version', '0.1')
    @mock.patch('sys.stdout')
    @mock.patch('elfws.display.datetime')
    def test_suppress(self, mock_datetime, mock_stdout):
        mock_datetime.now.return_value = 'Some Date'
        sys.argv = ['elfws', 'suppress', sWarningFile, sSupFile]
        __main__.main()

        lLogFile = utils.read_log_file('tests/elfws/suppress_output.txt')
        
        lExpected = []
        for sLine in lLogFile:
            lExpected.append(mock.call(sLine))
            lExpected.append(mock.call('\n'))

        mock_stdout.write.assert_has_calls(lExpected)

    @mock.patch('elfws.version.version', '0.1')
    @mock.patch('elfws.display.datetime')
    def test_report(self, mock_datetime):
        mock_datetime.now.return_value = 'Some Date'
        sys.argv = ['elfws', 'report', sWarningFile, 'tests/subcommand/report/suppress_microsemi_designer_logfile.yaml', sReportFile]
        __main__.main()

        lExpected = utils.read_log_file('tests/elfws/report_output.txt')
        lActual = utils.read_log_file(sReportFile)

        self.assertEqual(lExpected, lActual)

    @mock.patch('elfws.version.version', '0.1')
    @mock.patch('elfws.display.datetime')
    def test_report_all_warnings_suppressed(self, mock_datetime):
        mock_datetime.now.return_value = 'Some Date'
        sys.argv = ['elfws', 'report', sWarningFile, 'tests/elfws/suppress_all_microsemi_designer_warnings.yaml', sReportFile]
        __main__.main()

        lExpected = utils.read_log_file('tests/elfws/report_output_all_warnings_suppressed.txt')
        lActual = utils.read_log_file(sReportFile)

        self.assertEqual(lExpected, lActual)

    @mock.patch('elfws.version.version', '0.1')
    @mock.patch('elfws.display.datetime')
    def test_report_no_warnings(self, mock_datetime):
        mock_datetime.now.return_value = 'Some Date'
        sys.argv = ['elfws', 'report', 'tests/elfws/no_warnings/warning_messages.rpt', 'tests/elfws/no_warnings/suppression_file.yaml', sReportFile]
        __main__.main()

        lExpected = utils.read_log_file('tests/elfws/no_warnings/report_output.txt')
        lActual = utils.read_log_file(sReportFile)

        self.assertEqual(lExpected, lActual)

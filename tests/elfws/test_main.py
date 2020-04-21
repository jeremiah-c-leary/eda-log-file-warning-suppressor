
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

class test_arguments(unittest.TestCase):

    def setUp(self):
        if os.path.isfile(sYamlFile):
            os.remove(sYamlFile)
    
    def tearDown(self):
        if os.path.isfile(sYamlFile):
            os.remove(sYamlFile)

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

    def test_create_without_suppression_file(self):
        sys.argv = ['elfws', 'create', sWarningFile, sYamlFile]
        __main__.main()

        lExpected = utils.read_log_file('tests/elfws/create_yaml_wo_suppression.yaml')
        lActual = utils.read_log_file(sYamlFile)

        self.assertEqual(lExpected, lActual)

    def test_create_with_suppression_file(self):
        sys.argv = ['elfws', 'create', sWarningFile, sYamlFile, '--suppression_file', sSupFile]
        __main__.main()

        lExpected = utils.read_log_file('tests/elfws/create_yaml_with_suppression.yaml')
        lActual = utils.read_log_file(sYamlFile)

        self.assertEqual(lExpected, lActual)

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


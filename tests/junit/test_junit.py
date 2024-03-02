
import datetime
import os
import sys
import unittest
from unittest import mock

from elfws import __main__
from elfws import version
from elfws import utils

sWarningFile = os.path.join(os.path.dirname(__file__), 'warning_messages.log')

sXmlFile = 'deleteme.xml'

class test_arguments(unittest.TestCase):

    def setUp(self):
        if os.path.isfile(sXmlFile):
            os.remove(sXmlFile)
    
    def tearDown(self):
        if os.path.isfile(sXmlFile):
            os.remove(sXmlFile)

    @mock.patch('sys.stdout')
    def test_report_w_junit_output(self, mockStdout):
        sys.argv = ['elfws', 'show', sWarningFile, '--junit', sXmlFile]
        __main__.main()

        lExpected = utils.read_log_file(os.path.join(os.path.dirname(__file__), 'junit_output.xml'))
        lActual = utils.read_log_file(sXmlFile)

        self.assertEqual(len(lExpected), len(lActual))
        for iIndex, sLine in enumerate(lExpected):
            if not iIndex == 1:
                self.assertEqual(sLine, lActual[iIndex])


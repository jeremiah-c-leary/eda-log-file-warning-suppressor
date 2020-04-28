
import os
import unittest

from elfws.vendor.mentor_graphics import precision as tool
from tests import test_utils

lLogFile = test_utils.read_file(os.path.join(os.path.dirname(__file__), 'warning_messages.rpt'))

class testFunctions(unittest.TestCase):

    def test_extract_warnings(self):
        oWarningList = tool.extract_warnings(lLogFile)

        oWarning = oWarningList.warnings[0]
        self.assertEqual('15232', oWarning.get_id())
        self.assertEqual('Some warning message', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(5, oWarning.get_linenumber())

        self.assertEqual(2, oWarningList.get_number_of_warnings())

        oWarning = oWarningList.warnings[1]
        self.assertEqual('NO_ID', oWarning.get_id())
        self.assertEqual('Some warning that does not have an ID : some other text', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(6, oWarning.get_linenumber())

    def test_is_logfile(self):
        lLogFile = []
        lLogFile.append('')
        lLogFile.append('//  Precision RTL Synthesis 64-bit 2019.1.0.9...')
        lLogFile.append('//  ')

        self.assertTrue(tool.is_logfile(lLogFile))

        lLogFile = []
        lLogFile.append('')
        lLogFile.append('//  recision RTL Synthesis 64-bit 2019.1.0.9...')
        lLogFile.append('//  ')

        self.assertFalse(tool.is_logfile(lLogFile))

        lLogFile = []
        lLogFile.append('')
        lLogFile.append('')
        lLogFile.append('')
        lLogFile.append('//  recision RTL Synthesis 64-bit 2019.1.0.9...')
        lLogFile.append('//  ')
        lLogFile.append('')
        lLogFile.append('')
        lLogFile.append('')
        lLogFile.append('')
        lLogFile.append('')
        lLogFile.append('')
        lLogFile.append('')
        lLogFile.append('')
        lLogFile.append('')

        self.assertFalse(tool.is_logfile(lLogFile))

        lLogFile = []
        lLogFile.append('')
        lLogFile.append('//  Precision Hi-Rel 64-bit 2019.1.0.9...')
        lLogFile.append('//  ')

        self.assertTrue(tool.is_logfile(lLogFile))

    def test_get_vendor(self):
        self.assertEqual(['Mentor Graphics'], tool.get_vendor())

    def test_get_tool_name(self):
        self.assertEqual('precision', tool.get_tool_name())

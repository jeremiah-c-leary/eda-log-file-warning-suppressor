
import os
import unittest

from elfws.vendor.mentor_graphics import questa_lint as tool
from tests import test_utils

lLogFile = test_utils.read_file(os.path.join(os.path.dirname(__file__), 'warning_messages.rpt'))


class testFunctions(unittest.TestCase):

    def test_extract_warnings(self):
        oWarningList = tool.extract_warnings(lLogFile)

        oWarning = oWarningList.warnings[0]
        self.assertEqual('Something', oWarning.get_id())
        self.assertEqual('error report over multiple lines but separated by blank lines', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(12, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[1]
        self.assertEqual('Something', oWarning.get_id())
        self.assertEqual('Yet another error over multiple lines', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(16, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[2]
        self.assertEqual('other_error', oWarning.get_id())
        self.assertEqual('[blah blah] more extra lines', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(23, oWarning.get_linenumber())

        self.assertEqual(3, len(oWarningList.warnings))

    def test_is_logfile(self):
        lLogFile = []
        lLogFile.append('===========================================')
        lLogFile.append('Lint Check Report')
        lLogFile.append('Questa Lint  Version')
        lLogFile.append('')

        self.assertTrue(tool.is_logfile(lLogFile))

        lLogFile = []
        lLogFile.append('===========================================')
        lLogFile.append('Lint Check Report')
        lLogFile.append('uesta Lint  Version')
        lLogFile.append('')

        self.assertFalse(tool.is_logfile(lLogFile))

        lLogFile = []
        lLogFile.append('')
        lLogFile.append('')
        lLogFile.append('')
        lLogFile.append('Questa Lint Version')
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
        lLogFile.append('Questa Lint  Version')

        self.assertTrue(tool.is_logfile(lLogFile))

    def test_get_vendor(self):
        self.assertEqual(['Mentor Graphics'], tool.get_vendor())

    def test_get_tool_name(self):
        self.assertEqual('questa_lint', tool.get_tool_name())

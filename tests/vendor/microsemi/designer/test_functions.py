
import os
import unittest

from elfws.vendor.microsemi import designer
from tests import test_utils

lLogFile = test_utils.read_file(os.path.join(os.path.dirname(__file__), 'warning_messages.log'))

class testFunctions(unittest.TestCase):

    def test_extract_warnings(self):
        oWarningList = designer.extract_warnings(lLogFile)

        oWarning = oWarningList.warnings[0]
        self.assertEqual('DEF1234', oWarning.get_id())
        self.assertEqual('This is a warning', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(8, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[1]
        self.assertEqual('NO_ID', oWarning.get_id())
        self.assertEqual('This is a warning without an ID', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(11, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[2]
        self.assertEqual('NO_ID', oWarning.get_id())
        self.assertEqual('This is a warning with a : that does not have an ID', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(12, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[3]
        self.assertEqual('MULTI546', oWarning.get_id())
        self.assertEqual('This is the first line of the warning This is the second line of the warning This is the last line of the warning.', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(15, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[4]
        self.assertEqual('NO_ID', oWarning.get_id())
        self.assertEqual('This is the first line : of the message This is the second line of the message This is the third line of the message This is the last line of the message.', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(20, oWarning.get_linenumber())

        self.assertEqual(5, oWarningList.get_number_of_warnings())

    def test_is_logfile(self):
        lLogFile = []
        lLogFile.append('Microsemi Libero Software')
        lLogFile.append('Version: 11.9.2.1')
        lLogFile.append('11.9 SP2')
        lLogFile.append(' ')

        self.assertTrue(designer.is_logfile(lLogFile))

        lLogFile = []
        lLogFile.append('icrosemi Libero Software')
        lLogFile.append('Version: 11.9.2.1')
        lLogFile.append('11.9 SP2')
        lLogFile.append(' ')

        self.assertFalse(designer.is_logfile(lLogFile))

        lLogFile = []
        lLogFile.append(' ')
        lLogFile.append(' ')
        lLogFile.append('icrosemi Libero Software')
        lLogFile.append('Version: 11.9.2.1')
        lLogFile.append('11.9 SP2')
        lLogFile.append(' ')
        lLogFile.append(' ')
        lLogFile.append(' ')
        lLogFile.append(' ')
        lLogFile.append(' ')
        lLogFile.append(' ')
        lLogFile.append(' ')
        lLogFile.append(' ')

        self.assertFalse(designer.is_logfile(lLogFile))

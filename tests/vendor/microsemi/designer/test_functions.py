
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

    def test_extract_warnings_on_last_line(self):
        lLogFile = []
        lLogFile.append('Microsemi Libero Software')
        lLogFile.append('Warning: ABC: warning on last line')
        oWarningList = designer.extract_warnings(lLogFile)
        self.assertEqual(1, oWarningList.get_number_of_warnings())
        self.assertEqual('ABC', oWarningList.warnings[0].get_id())
        self.assertEqual('warning on last line', oWarningList.warnings[0].get_message())
        self.assertEqual(2, oWarningList.warnings[0].get_linenumber())

    def test_extract_multiline_warning_at_end_of_file(self):
        lLogFile = []
        lLogFile.append('Microsemi Libero Software')
        lLogFile.append('Warning: ABC: first line')
        lLogFile.append('         second line')
        oWarningList = designer.extract_warnings(lLogFile)
        self.assertEqual(1, oWarningList.get_number_of_warnings())
        self.assertEqual('first line second line', oWarningList.warnings[0].get_message())

    def test_extract_id_and_message(self):
        self.assertEqual(('ABC', 'msg: with colon'), designer.extract_id_and_message('Warning: ABC: msg: with colon'))
        self.assertEqual(('ABC', ''), designer.extract_id_and_message('Warning: ABC:'))
        self.assertEqual(('NO_ID', 'has spaces: msg'), designer.extract_id_and_message('Warning: has spaces: msg'))
        self.assertEqual(('NO_ID', 'no separator'), designer.extract_id_and_message('Warning: no separator'))

    def test_back_to_back_multiline_warnings(self):
        oWarningList = designer.extract_warnings(['Warning: A: one', '   more', 'Warning: B: two', '   end'])
        lActual = [(o.get_id(), o.get_message(), o.get_linenumber()) for o in oWarningList.get_warnings()]
        self.assertEqual([('A', 'one more', 1), ('B', 'two end', 3)], lActual)

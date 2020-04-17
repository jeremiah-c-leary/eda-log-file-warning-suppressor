
import os
import unittest

from elfws.vendor.microsemi import designer
from tests import utils

lLogFile = utils.read_file(os.path.join(os.path.dirname(__file__), 'warning_messages.log'))

class testFunctions(unittest.TestCase):

    def test_extract_warnings(self):
        oWarningList = designer.extract_warnings(lLogFile)

        oWarning = oWarningList.warnings[0]
        self.assertEqual('DEF1234', oWarning.get_id())
        self.assertEqual('This is a warning', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(4, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[1]
        self.assertEqual('NO_ID', oWarning.get_id())
        self.assertEqual('This is a warning without an ID', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(7, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[2]
        self.assertEqual('NO_ID', oWarning.get_id())
        self.assertEqual('This is a warning with a : that does not have an ID', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(8, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[3]
        self.assertEqual('MULTI546', oWarning.get_id())
        self.assertEqual('This is the first line of the warning This is the second line of the warning This is the last line of the warning.', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(11, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[4]
        self.assertEqual('NO_ID', oWarning.get_id())
        self.assertEqual('This is the first line : of the message This is the second line of the message This is the third line of the message This is the last line of the message.', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(16, oWarning.get_linenumber())

        self.assertEqual(5, oWarningList.get_number_of_warnings())


import os
import unittest

from elfws.vendor.synopsys import synplify_pro
from tests import test_utils

lLogFile = test_utils.read_file(os.path.join(os.path.dirname(__file__), 'warning_messages.log'))

class testFunctions(unittest.TestCase):

    def test_extract_warnings(self):
        oWarningList = synplify_pro.extract_warnings(lLogFile)

        oWarning = oWarningList.warnings[0]
        self.assertEqual('ID1', oWarning.get_id())
        self.assertEqual('"file name" some message', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(7, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[1]
        self.assertEqual('ID1', oWarning.get_id())
        self.assertEqual('"file name" some other message', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(10, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[2]
        self.assertEqual('ID2', oWarning.get_id())
        self.assertEqual('Some message without a file', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(11, oWarning.get_linenumber())

    def test_is_logfile(self):
        lLogFile = []
        lLogFile.append('#Build: Synplify Pro (R)')
        lLogFile.append('#OS:')

        self.assertTrue(synplify_pro.is_logfile(lLogFile))

        lLogFile = []
        lLogFile.append('#OS: ')
        lLogFile.append('#install')

        self.assertFalse(synplify_pro.is_logfile(lLogFile))

        lLogFile = []
        lLogFile.append('#Build: Synplify (R)')
        lLogFile.append('#OS:')

        self.assertFalse(synplify_pro.is_logfile(lLogFile))


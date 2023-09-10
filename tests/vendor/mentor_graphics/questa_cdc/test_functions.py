
import os
import unittest

from elfws.vendor.mentor_graphics import questa_cdc as tool
from tests import test_utils

lLogFile = test_utils.read_file(os.path.join(os.path.dirname(__file__), 'warning_messages.rpt'))


class testFunctions(unittest.TestCase):

    def test_extract_warnings(self):
        oWarningList = tool.extract_warnings(lLogFile)

        oWarning = oWarningList.warnings[0]
        self.assertEqual('Clock_Information', oWarning.get_id())
        self.assertEqual(' 2. Inferred                      :(1)', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(33, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[1]
        self.assertEqual('Reset_Information', oWarning.get_id())
        self.assertEqual(' 2. Inferred                      :(1)', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(44, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[2]
        self.assertEqual('CDC_Violations', oWarning.get_id())
        self.assertEqual('name of first violation cdc check  (2)', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(55, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[3]
        self.assertEqual('CDC_Violations', oWarning.get_id())
        self.assertEqual('name of second violation cdc check (1)', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(56, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[4]
        self.assertEqual('CDC_Cautions', oWarning.get_id())
        self.assertEqual('name of first caution cdc check  (2)', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(60, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[5]
        self.assertEqual('CDC_Cautions', oWarning.get_id())
        self.assertEqual('name of second caution cdc check (1)', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(61, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[6]
        self.assertEqual('CDC_Evaluations', oWarning.get_id())
        self.assertEqual('name of first evaluation cdc check  (2)', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(65, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[7]
        self.assertEqual('CDC_Evaluations', oWarning.get_id())
        self.assertEqual('name of second evaluation cdc check (1)', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(66, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[8]
        self.assertEqual('Design_Information', oWarning.get_id())
        self.assertEqual('Number of Empty Modules      = 10', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(94, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[9]
        self.assertEqual('Design_Information', oWarning.get_id())
        self.assertEqual('Number of Unresolved Modules = 5', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(95, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[10]
        self.assertEqual('Port_Domain_Information', oWarning.get_id())
        self.assertEqual('I_A       input       clock      { domain_a }    User', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(102, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[11]
        self.assertEqual('Port_Domain_Information', oWarning.get_id())
        self.assertEqual('O_A       output                 { domain_b }    User', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(105, oWarning.get_linenumber())

        self.assertEqual(12, len(oWarningList.warnings))

    def test_is_logfile(self):
        lLogFile = []
        lLogFile.append('===========================================')
        lLogFile.append('Questa CDC Version')
        lLogFile.append('Clock Domain Crossing Analysis Report.')
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
        lLogFile.append('Questa CDC Version')
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


    def test_get_vendor(self):
        self.assertEqual(['Mentor Graphics'], tool.get_vendor())

    def test_get_tool_name(self):
        self.assertEqual('questa_cdc', tool.get_tool_name())

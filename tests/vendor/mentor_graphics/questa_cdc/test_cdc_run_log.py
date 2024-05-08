
import os
import unittest

from elfws.vendor.mentor_graphics import questa_cdc__cdc_run_log as tool
from tests import test_utils

lLogFile = test_utils.read_file(os.path.join(os.path.dirname(__file__), 'cdc_run.log'))


class testFunctions(unittest.TestCase):

    def test_extract_warnings(self):
        oWarningList = tool.extract_warnings(lLogFile)

        oWarning = oWarningList.warnings[0]
        self.assertEqual('cdc_violations', oWarning.get_id())
        self.assertEqual('name of first violation cdc check  (2)', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(22, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[1]
        self.assertEqual('cdc_violations', oWarning.get_id())
        self.assertEqual('name of second violation cdc check (1)', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(23, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[2]
        self.assertEqual('cdc_cautions', oWarning.get_id())
        self.assertEqual('name of first caution cdc check  (2)', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(27, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[3]
        self.assertEqual('cdc_cautions', oWarning.get_id())
        self.assertEqual('name of second caution cdc check (1)', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(28, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[4]
        self.assertEqual('cdc_evaluations', oWarning.get_id())
        self.assertEqual('name of first evaluation cdc check  (2)', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(32, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[5]
        self.assertEqual('cdc_evaluations', oWarning.get_id())
        self.assertEqual('name of second evaluation cdc check (1)', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(33, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[6]
        self.assertEqual('warning_check', oWarning.get_id())
        self.assertEqual('    2  Warning id2                    warning#1', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(57, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[7]
        self.assertEqual('warning_check', oWarning.get_id())
        self.assertEqual('    5  Warning id5                    warning#2', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(60, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[8]
        self.assertEqual('error_check', oWarning.get_id())
        self.assertEqual('    3  Error   id3                    error#1', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(58, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[9]
        self.assertEqual('error_check', oWarning.get_id())
        self.assertEqual('    6  Error   id6                    error#2', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(61, oWarning.get_linenumber())

        self.assertEqual(10, len(oWarningList.warnings))

    def test_is_logfile(self):
        lLogFile = []
        lLogFile.append('#')
        lLogFile.append('# Questa Static Verification System')
        lLogFile.append('# Version 2022.1_2')
        lLogFile.append('')
        lLogFile.append('')
        lLogFile.append('  -tool cdc')
        lLogFile.append('')
        lLogFile.append('')
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

        lLogFile = []
        lLogFile.append('===========================================')
        lLogFile.append('Questa CDC Version')
        lLogFile.append('Clock Domain Crossing Analysis Report.')
        lLogFile.append('')

        self.assertFalse(tool.is_logfile(lLogFile))

    def test_is_2023_logfile(self):
        lLogFile = []
        lLogFile.append('#')
        lLogFile.append('# Questa Static Verification System')
        lLogFile.append('# Version 2022.1_2')
        lLogFile.append('log created  ')
        lLogFile.append('')
        lLogFile.append('Executing Command : cdc run')
        lLogFile.append('')
        lLogFile.append('')
        lLogFile.append('')

        self.assertTrue(tool.is_logfile(lLogFile))

    def test_get_vendor(self):
        self.assertEqual(['Mentor Graphics'], tool.get_vendor())

    def test_get_tool_name(self):
        self.assertEqual('questa_cdc', tool.get_tool_name())

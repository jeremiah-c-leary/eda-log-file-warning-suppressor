import os
import unittest

from elfws.vendor.xilinx import vivado
from tests import test_utils

lLogFile = test_utils.read_file(os.path.join(os.path.dirname(__file__), 'warning_messages.rpt'))

class testFunctions(unittest.TestCase):

    def test_extract_warnings(self):
        oWarningList = vivado.extract_warnings(lLogFile)

        oWarning = oWarningList.warnings[0]
        self.assertEqual('SYN: 8-5678', oWarning.get_id())
        self.assertEqual('This is a single line message', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(3, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[1]
        self.assertEqual('SYN 8-4352', oWarning.get_id())
        self.assertEqual('This is another single line message', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(5, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[2]
        self.assertEqual('IMPL 567-1324', oWarning.get_id())
        self.assertEqual('This is a single line message with a tab on the next line', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(7, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[3]
        self.assertEqual('ABCD 9324-asdf562', oWarning.get_id())
        self.assertEqual('This is a critical warning', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(10, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[4]
        self.assertEqual('XPM_CDC_SINGLE: TCL-1000', oWarning.get_id())
        self.assertEqual('First line Second line third line fourth line fifth line', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(14, oWarning.get_linenumber())

        self.assertEqual(5, oWarningList.get_number_of_warnings())

    def test_is_logfile(self):
        lLogFile = []
        lLogFile.append('****** Vivado v2018.3 (64-bit)')
        lLogFile.append('  **** SW Build 2405991 on ')
        lLogFile.append('  **** IP Build 2404404 on ')
        lLogFile.append('   ** Copyright ')

        self.assertTrue(vivado.is_logfile(lLogFile))

        lLogFile = []
        lLogFile.append('***** Vivado v2018.3 (64-bit)')
        lLogFile.append('  **** SW Build 2405991 on ')
        lLogFile.append('  **** IP Build 2404404 on ')
        lLogFile.append('   ** Copyright ')

        self.assertFalse(vivado.is_logfile(lLogFile))

        lLogFile = []
        lLogFile.append(' ')
        lLogFile.append(' ')
        lLogFile.append('***** Vivado v2018.3 (64-bit)')
        lLogFile.append('  **** SW Build 2405991 on ')
        lLogFile.append('  **** IP Build 2404404 on ')
        lLogFile.append('   ** Copyright ')
        lLogFile.append(' ')
        lLogFile.append(' ')
        lLogFile.append(' ')
        lLogFile.append(' ')
        lLogFile.append(' ')
        lLogFile.append(' ')
        lLogFile.append(' ')
        lLogFile.append(' ')

        self.assertFalse(vivado.is_logfile(lLogFile))

        lLogFile = []
        for i in range(0, 100):
            lLogFile.append('  ')
        lLogFile.append('# Vivado ')
        lLogFile.append('# SW Build ')
        lLogFile.append('# IP Build ')
        lLogFile.append('# Process ID: ')

        self.assertTrue(vivado.is_logfile(lLogFile))

        lLogFile = []
        for i in range(0, 300):
            lLogFile.append('')

        self.assertFalse(vivado.is_logfile(lLogFile))

    def test_vendor(self):
        self.assertEqual(['Xilinx'], vivado.get_vendor())

    def test_tool_name(self):
        self.assertEqual('vivado', vivado.get_tool_name())

    def test_extract_warnings_on_last_line(self):
        lLogFile = []
        lLogFile.append('****** Vivado v2018.3 (64-bit)')
        lLogFile.append('WARNING: [Synth 8-1] first warning')
        lLogFile.append('WARNING: [Synth 8-2] warning on last line')
        oWarningList = vivado.extract_warnings(lLogFile)
        self.assertEqual(2, oWarningList.get_number_of_warnings())
        self.assertEqual('Synth 8-2', oWarningList.warnings[1].get_id())
        self.assertEqual('warning on last line', oWarningList.warnings[1].get_message())
        self.assertEqual(3, oWarningList.warnings[1].get_linenumber())

    def test_extract_multiline_warning_at_end_of_file(self):
        lLogFile = []
        lLogFile.append('****** Vivado v2018.3 (64-bit)')
        lLogFile.append('CRITICAL WARNING: [Synth 8-3] first line')
        lLogFile.append('    second line')
        oWarningList = vivado.extract_warnings(lLogFile)
        self.assertEqual(1, oWarningList.get_number_of_warnings())
        self.assertEqual('first line second line', oWarningList.warnings[0].get_message())

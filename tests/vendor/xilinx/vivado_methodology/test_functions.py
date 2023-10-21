import os
import unittest

from elfws.vendor.xilinx import vivado_methodology
from tests import test_utils

lLogFile = test_utils.read_file(os.path.join(os.path.dirname(__file__), 'warning_messages.rpt'))

class testFunctions(unittest.TestCase):

    def test_extract_warnings(self):
        oWarningList = vivado_methodology.extract_warnings(lLogFile)

        oWarning = oWarningList.warnings[0]
        self.assertEqual('TIMING-18', oWarning.get_id())
        self.assertEqual('An input delay is missing on I_CS_F relative to clock(s) I_CLK', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(37, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[1]
        self.assertEqual('TIMING-18', oWarning.get_id())
        self.assertEqual('An input delay is missing on I_DATA relative to clock(s) I_CLK', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(42, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[2]
        self.assertEqual('TIMING-18', oWarning.get_id())
        self.assertEqual('An input delay is missing on I_MISO_DATA relative to clock(s) I_CLK', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(47, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[3]
        self.assertEqual('TIMING-18', oWarning.get_id())
        self.assertEqual('An input delay is missing on I_RST relative to clock(s) I_CLK', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(52, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[4]
        self.assertEqual('TIMING-18', oWarning.get_id())
        self.assertEqual('An input delay is missing on I_SCK relative to clock(s) I_CLK', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(57, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[5]
        self.assertEqual('TIMING-18', oWarning.get_id())
        self.assertEqual('An output delay is missing on O_DATA relative to clock(s) I_CLK', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(62, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[6]
        self.assertEqual('TIMING-18', oWarning.get_id())
        self.assertEqual('An output delay is missing on O_MOSI_CLK relative to clock(s) I_CLK', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(67, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[7]
        self.assertEqual('TIMING-19', oWarning.get_id())
        self.assertEqual('An output delay is missing on O_MOSI_CS_F relative to clock(s) I_CLK', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(72, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[8]
        self.assertEqual('TIMING-20', oWarning.get_id())
        self.assertEqual('An output delay is missing on O_MOSI_DATA relative to clock(s) I_CLK', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(77, oWarning.get_linenumber())

        self.assertEqual(9, oWarningList.get_number_of_warnings())

    def test_is_logfile(self):
        lLogFile = []
        lLogFile.append('Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.')
        lLogFile.append('-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        lLogFile.append('| Tool Version : Vivado v.2020.2 (win64) Build 3064766 Wed Nov 18 09:12:45 MST 2020')
        lLogFile.append('| Date         : Sun Aug 13 10:00:30 2023')
        lLogFile.append('| Host         : DESKTOP-HV9NHA3 running 64-bit major release  (build 9200)')
        lLogFile.append('| Command      : report_methodology -file four_wire_spi_methodology_drc_routed.rpt -pb four_wire_spi_methodology_drc_routed.pb -rpx four_wire_spi_methodology_drc_routed.rpx')
        lLogFile.append('| Design       : four_wire_spi')
        lLogFile.append('| Device       : xa7a12tcpg238-2I')
        lLogFile.append('| Speed File   : -2I')
        lLogFile.append('| Design State : Fully Routed')
        lLogFile.append('-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        lLogFile.append(' ')
        lLogFile.append('Report Methodology')

        self.assertTrue(vivado_methodology.is_logfile(lLogFile))

        lLogFile = []
        lLogFile.append('***** Vivado v2018.3 (64-bit)')
        lLogFile.append('  **** SW Build 2405991 on ')
        lLogFile.append('  **** IP Build 2404404 on ')
        lLogFile.append('   ** Copyright ')

        self.assertFalse(vivado_methodology.is_logfile(lLogFile))

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

        self.assertFalse(vivado_methodology.is_logfile(lLogFile))

        lLogFile = []
        for i in range(0, 100):
            lLogFile.append('  ')
        lLogFile.append('# Vivado ')
        lLogFile.append('# SW Build ')
        lLogFile.append('# IP Build ')
        lLogFile.append('# Process ID: ')

        self.assertFalse(vivado_methodology.is_logfile(lLogFile))

        lLogFile = []
        for i in range(0, 300):
            lLogFile.append('')

        self.assertFalse(vivado_methodology.is_logfile(lLogFile))

    def test_vendor(self):
        self.assertEqual(['Xilinx'], vivado_methodology.get_vendor())

    def test_tool_name(self):
        self.assertEqual('vivado', vivado_methodology.get_tool_name())

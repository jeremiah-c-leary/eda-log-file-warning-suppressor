
import unittest


from elfws import display
from elfws import version
from elfws import log_file
from elfws import parser_loader
from elfws import rule_matching
from elfws import suppression_file
from elfws import suppression
from elfws import warning
from elfws import warning_list


class test_functions(unittest.TestCase):

    def test_build_header(self):
        lExpected = []
        lExpected.append('='*80)
        lExpected.append('ELFWS version         : ' + version.version)
        lExpected.append('Date                  : ')
        lExpected.append('Log file              : some_log_file.log')
        lExpected.append('Suppression Rule File : some_rule_file.yaml')
        lExpected.append('')

        lActual = display.build_header('some_log_file.log', 'some_rule_file.yaml')

        for iIndex, sLine in enumerate(lExpected):
            if iIndex == 2:
                self.assertEqual(sLine[:23], lActual[iIndex][:23])
            else:
                self.assertEqual(sLine, lActual[iIndex])

    def test_build_warning_table_with_warnings(self):
        lExpected = []
        lExpected.append('-'*17 + '+' + '-'*8 + '+' + '-'*(80 - 20 - 1 - 5 - 1))
        lExpected.append(' ID              | Line # | Warning Message')
        lExpected.append('-'*17 + '+' + '-'*8 + '+' + '-'*(80 - 20 - 1 - 5 - 1))
        lExpected.append(' DEF1234         |      8 | This is a warning')
        lExpected.append(' NO_ID           |     11 | This is a warning without an ID')
        lExpected.append(' NO_ID           |     12 | This is a warning with a : that does not have an ID')
        lExpected.append(' MULTI546        |     15 | This is the first line of the warning This is the second line of the warning This is the last line of the warning.')
        lExpected.append(' NO_ID           |     20 | This is the first line : of the message This is the second line of the message This is the third line of the message This is the last line of the message.')
        lExpected.append('-'*17 + '+' + '-'*8 + '+' + '-'*(80 - 20 - 1 - 5 - 1))
        lExpected.append('')

        lLogFile = log_file.read_log_file('tests/vendor/microsemi/designer/warning_messages.log')

        mTool = parser_loader.get_vendor_tool_module(lLogFile)
        oWarnList = mTool.extract_warnings(lLogFile)
        lWarnList = oWarnList.get_warnings()

        lActual = display.build_warning_table(lWarnList)

        self.assertEqual(len(lExpected), len(lActual))

        for iIndex, sLine in enumerate(lExpected):
            self.assertEqual(sLine, lActual[iIndex])

    def test_build_warning_table_with_no_warnings(self):
        lExpected = []

        oWarnList = warning_list.WarningList()
        lWarnList = oWarnList.get_warnings()

        lActual = display.build_warning_table(lWarnList)

        self.assertEqual(len(lExpected), len(lActual))

        for iIndex, sLine in enumerate(lExpected):
            self.assertEqual(sLine, lActual[iIndex])

    def test_build_table_of_contents(self):
        lExpected = []
        lExpected.append('Table of Contents:')
        lExpected.append('')
        lExpected.append('  1.  Unsuppressed Warnings')
        lExpected.append('  2.  Suppressed Warnings')
        lExpected.append('  3.  Unused Suppression Rules')
        lExpected.append('  4.  Warnings Under Investigation')
        lExpected.append('  5.  Warnings Suppressed by Multiple Rules')
        lExpected.append('  6.  Summary')
        lExpected.append('')

        self.assertEqual(lExpected, display.build_table_of_contents())

    def test_build_report_section_divider(self):
        lExpected = []
        lExpected.append('-'*80)
        lExpected.append(' 1. Unsuppressed Warnings')
        lExpected.append('-'*80)
        lExpected.append('')

        self.assertEqual(lExpected, display.build_report_section_divider('1. Unsuppressed Warnings'))


    def test_build_suppressed_warning_header(self):
        lExpected = []
        lExpected.append('~'*80)
        lExpected.append('Suppression Author  : jcleary')
        lExpected.append('Suppression Comment : This is fine because...')
        lExpected.append('Suppression Rule    : Some warning mess')
        lExpected.append('')

        oSup = suppression.Suppression(None, 'Some warning mess', 'jcleary', 'This is fine because...')

        self.assertEqual(lExpected, display.build_suppressed_warning_header(oSup))

    def test_build_suppressed_warning_table(self):
        lExpected = []
        lExpected.append('-'*17 + '+' + '-'*8 + '+' + '-'*(80 - 20 - 1 - 5 - 1))
        lExpected.append(' ID              | Line # | Warning Message')
        lExpected.append('-'*17 + '+' + '-'*8 + '+' + '-'*(80 - 20 - 1 - 5 - 1))
        lExpected.append(' CMP001          |      1 | message 1')
        lExpected.append(' CMP002          |      2 | message 2')
        lExpected.append(' CMP003          |      3 | message 3')
        lExpected.append(' CMP004          |      4 | message 4')
        lExpected.append(' CMP005          |      5 | message 5')
        lExpected.append('-'*17 + '+' + '-'*8 + '+' + '-'*(80 - 20 - 1 - 5 - 1))
        lExpected.append('')

        oSup = suppression.Suppression()
        oSup.add_suppressed_warning(warning.LogWarning('CMP001', 'message 1', None, 1))
        oSup.add_suppressed_warning(warning.LogWarning('CMP002', 'message 2', None, 2))
        oSup.add_suppressed_warning(warning.LogWarning('CMP003', 'message 3', None, 3))
        oSup.add_suppressed_warning(warning.LogWarning('CMP004', 'message 4', None, 4))
        oSup.add_suppressed_warning(warning.LogWarning('CMP005', 'message 5', None, 5))

        lActual = display.build_suppressed_warning_table(oSup)

        for iIndex, sLine in enumerate(lExpected):
            self.assertEqual(sLine, lActual[iIndex])


    def test_build_suppression_item(self):
        lExpected = []
        lExpected.append('Warning ID : CMD001')
        lExpected.append('Author     : jcleary')
        lExpected.append('Rule       : .*Some.*')
        lExpected.append('Comment    : This is good because...')
        lExpected.append('')

        oSup = suppression.Suppression('CMD001', 'Some', 'jcleary', 'This is good because...')

        lActual = display.build_suppression_item(oSup, 0)

        for iIndex, sLine in enumerate(lExpected):
            self.assertEqual(sLine, lActual[iIndex])


    def test_build_multiply_suppressed_warning_header(self):
        lExpected = []
        lExpected.append('~'*80)
        lExpected.append('Warning ID  : SYN001')
        lExpected.append('Line Number : 54')
        lExpected.append('Message     : Some warning message')
        lExpected.append('')

        oWarning = warning.LogWarning('SYN001', 'Some warning message', None, 54)

        lActual = display.build_multiply_suppressed_warning_header(oWarning)

        for iIndex, sLine in enumerate(lExpected):
            self.assertEqual(sLine, lActual[iIndex])


    def test_build_report_summary_section(self):
        lExpected = []
        lExpected.append('  Suppression Rules')
        lExpected.append('    Total                  :     6')
        lExpected.append('    Unused                 :     1')
        lExpected.append('')
        lExpected.append('  Warnings')
        lExpected.append('    Total                  :     5')
        lExpected.append('    Suppressed             :     4')
        lExpected.append('    Unsuppressed           :     1')
        lExpected.append('    Under Investigation    :     0')
        lExpected.append('    Multiply Suppressed    :     3')
        lExpected.append('')
        lExpected.append('='*80)

        oSupList = suppression_file.create_suppression_list(suppression_file.read_suppression_file('tests/subcommand/report/suppress_microsemi_designer_logfile.yaml'))
        oWarnList = parser_loader.create_warning_list(log_file.read_log_file('tests/vendor/microsemi/designer/warning_messages.log'), 'tests/vendor/microsemi/designer/warning_messages.log')


        rule_matching.apply_suppression_rules_to_warnings(oWarnList, oSupList)

        lActual = display.build_report_summary_section(oWarnList, oSupList)

        for iIndex, sLine in enumerate(lExpected):
            self.assertEqual(sLine, lActual[iIndex])

    def test_maximum_id_length(self):
        self.assertEqual(0, display.maximum_id_length([]))
        self.assertEqual(1, display.maximum_id_length([warning.LogWarning('1')]))
        self.assertEqual(13, display.maximum_id_length([warning.LogWarning('11111'), warning.LogWarning('1111111111111'), warning.LogWarning('1')]))

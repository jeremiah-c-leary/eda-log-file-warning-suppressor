
import unittest


from elfws import display
from elfws import version
from elfws import utils
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

        lLogFile = utils.read_log_file('tests/vendor/microsemi/designer/warning_messages.log')

        mTool = utils.get_vendor_tool_module(lLogFile)
        oWarnList = mTool.extract_warnings(lLogFile)
        lWarnList = oWarnList.get_warnings()

        lActual = display.build_warning_table(lWarnList)

        self.assertEqual(len(lExpected), len(lActual))

        for iIndex, sLine in enumerate(lExpected):
            self.assertEqual(sLine, lActual[iIndex])

    def test_build_warning_table_with_no_warnings(self):
        lExpected = []

        oWarnList = warning_list.create()
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
        lExpected.append('  4.  Warnings Suppressed by Multiple Rules')
        lExpected.append('  5.  Summary')
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

        oSup = suppression.create(None, 'Some warning mess', 'jcleary', 'This is fine because...')

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

        oSup = suppression.create()
        oSup.add_suppressed_warning(warning.create('CMP001', 'message 1', None, 1))
        oSup.add_suppressed_warning(warning.create('CMP002', 'message 2', None, 2))
        oSup.add_suppressed_warning(warning.create('CMP003', 'message 3', None, 3))
        oSup.add_suppressed_warning(warning.create('CMP004', 'message 4', None, 4))
        oSup.add_suppressed_warning(warning.create('CMP005', 'message 5', None, 5))

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

        oSup = suppression.create('CMD001', 'Some', 'jcleary', 'This is good because...')

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

        oWarning = warning.create('SYN001', 'Some warning message', None, 54)

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
        lExpected.append('    Multiply Suppressed    :     3')
        lExpected.append('')
        lExpected.append('='*80)

        oSupList = utils.create_suppression_list(utils.read_suppression_file('tests/subcommand/report/suppress_microsemi_designer_logfile.yaml'))
        oWarnList = utils.create_warning_list(utils.read_log_file('tests/vendor/microsemi/designer/warning_messages.log'), 'tests/vendor/microsemi/designer/warning_messages.log')


        utils.apply_suppression_rules_to_warnings(oWarnList, oSupList)

        lActual = display.build_report_summary_section(oWarnList, oSupList)

        for iIndex, sLine in enumerate(lExpected):
            self.assertEqual(sLine, lActual[iIndex])




import unittest


from elfws import display
from elfws import version
from elfws import utils


class test_functions(unittest.TestCase):

    def test_build_header(self):
        lExpected = []
        lExpected.append('='*80)
        lExpected.append('ELFWS version         : ' + version.version)
        lExpected.append('Log file              : some_log_file.log')
        lExpected.append('Suppression Rule File : some_rule_file.yaml')
        lExpected.append('')

        self.assertEqual(lExpected, display.build_header('some_log_file.log', 'some_rule_file.yaml'))


    def test_build_warning_table(self):
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

        lLogFile = utils.read_log_file('tests/vendor/microsemi/designer/warning_messages.log')

        mTool = utils.get_vendor_tool_module(lLogFile)
        oWarnList = mTool.extract_warnings(lLogFile)

        lActual = display.build_warning_table(oWarnList)

        self.assertEqual(len(lExpected), len(lActual))

        for iIndex, sLine in enumerate(lExpected):
            self.assertEqual(sLine, lActual[iIndex])


    def test_build_footer(self):
        lExpected = []
        lExpected.append('')
        lExpected.append('Total Warnings        :   200')
        lExpected.append('Suppressed Warnings   :   195')
        lExpected.append('Unsuppressed Warnings :     5')
        lExpected.append('='*80)
        
        lLogFile = utils.read_log_file('tests/vendor/microsemi/designer/warning_messages.log')
        mTool = utils.get_vendor_tool_module(lLogFile)
        oWarnList = mTool.extract_warnings(lLogFile)

        lActual = display.build_footer(200, oWarnList)
        
        self.assertEqual(len(lExpected), len(lActual))

        for iIndex, sLine in enumerate(lExpected):
            self.assertEqual(sLine, lActual[iIndex])

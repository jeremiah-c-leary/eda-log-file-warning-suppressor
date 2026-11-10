
import os
import unittest

from elfws.vendor.mentor_graphics import questa_lint as tool
from tests import test_utils

lLogFile = test_utils.read_file(os.path.join(os.path.dirname(__file__), 'warning_messages.rpt'))


class testFunctions(unittest.TestCase):

    def test_extract_warnings(self):
        oWarningList = tool.extract_warnings(lLogFile)

        oWarning = oWarningList.warnings[0]
        self.assertEqual('Something', oWarning.get_id())
        self.assertEqual('error report over multiple lines but separated by blank lines', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(12, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[1]
        self.assertEqual('Something', oWarning.get_id())
        self.assertEqual('Yet another error over multiple lines', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(16, oWarning.get_linenumber())

        oWarning = oWarningList.warnings[2]
        self.assertEqual('other_error', oWarning.get_id())
        self.assertEqual('[blah blah] more extra lines', oWarning.get_message())
        self.assertEqual(None, oWarning.get_filename())
        self.assertEqual(23, oWarning.get_linenumber())

        self.assertEqual(3, len(oWarningList.warnings))

    def test_is_logfile(self):
        lLogFile = []
        lLogFile.append('===========================================')
        lLogFile.append('Lint Check Report')
        lLogFile.append('Questa Lint  Version')
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
        lLogFile.append('Questa Lint Version')
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
        lLogFile.append('Questa Lint  Version')

        self.assertTrue(tool.is_logfile(lLogFile))

    def test_get_vendor(self):
        self.assertEqual(['Mentor Graphics'], tool.get_vendor())

    def test_get_tool_name(self):
        self.assertEqual('questa_lint', tool.get_tool_name())

    def test_extract_warning_at_end_of_file(self):
        lLogFile = []
        lLogFile.append('Questa Lint  Version 2023')
        lLogFile.append('Section 2')
        lLogFile.append('Check: Something_A [Category: ...]')
        lLogFile.append('--------------------------------------------------')
        lLogFile.append('Something_A: error report over')
        lLogFile.append('multiple lines')
        oWarningList = tool.extract_warnings(lLogFile)
        self.assertEqual(1, oWarningList.get_number_of_warnings())
        self.assertEqual('Something_A', oWarningList.warnings[0].get_id())
        self.assertEqual('error report over multiple lines', oWarningList.warnings[0].get_message())
        self.assertEqual(5, oWarningList.warnings[0].get_linenumber())

    def test_extract_warning_directly_before_info_section(self):
        lLogFile = []
        lLogFile.append('Questa Lint  Version 2023')
        lLogFile.append('Section 2')
        lLogFile.append('Check: Something_A [Category: ...]')
        lLogFile.append('--------------------------------------------------')
        lLogFile.append('Something_A: last warning')
        lLogFile.append('| Info (#) |')
        oWarningList = tool.extract_warnings(lLogFile)
        self.assertEqual(1, oWarningList.get_number_of_warnings())
        self.assertEqual('last warning', oWarningList.warnings[0].get_message())

    def build_report(self, lLintCheckLines):
        return ['Questa Lint  Version 2023', 'Section 2'] + lLintCheckLines

    def extract(self, lLintCheckLines):
        return [(o.get_id(), o.get_message(), o.get_linenumber()) for o in tool.extract_warnings(self.build_report(lLintCheckLines)).get_warnings()]

    def test_warnings_without_blank_line_between_are_both_extracted(self):
        lActual = self.extract(['Check: A [x]', '----', 'A: first', 'A: second', ''])
        self.assertEqual([('A', 'first', 5), ('A', 'second', 6)], lActual)

    def test_message_ends_at_next_check(self):
        lActual = self.extract(['Check: A [x]', '----', 'A: first part', 'Check: B [x]', 'more', ''])
        self.assertEqual([('A', 'first part', 5)], lActual)

    def test_check_id_must_be_followed_by_colon(self):
        lActual = self.extract(['Check: A [x]', '----', 'A: msg', '', 'ABC: not a warning', ''])
        self.assertEqual([('A', 'msg', 5)], lActual)

    def test_no_warnings_before_first_check(self):
        self.assertEqual([], self.extract(['elfws: odd', '']))

    def test_no_warnings_without_section_2(self):
        self.assertEqual([], [o for o in tool.extract_warnings(['Questa Lint  Version 2023', 'Check: A [x]', 'A: msg', '']).get_warnings()])

    def test_lint_check_extracts_its_own_warnings(self):
        oLintCheck = tool.LintCheck('A')
        oLintCheck.add_line(10, '----')
        oLintCheck.add_line(11, 'A: first line')
        oLintCheck.add_line(12, 'second line')
        oLintCheck.add_line(13, '')
        oLintCheck.add_line(14, 'A: another')
        lActual = [(o.get_id(), o.get_message(), o.get_linenumber()) for o in oLintCheck.extract_warnings()]
        self.assertEqual([('A', 'first line second line', 11), ('A', 'another', 14)], lActual)

    def test_extract_lint_checks(self):
        lWarningSection = [(1, 'ignored'), (2, 'Check: A [x]'), (3, 'A: one'), (4, 'Check: B [y]'), (5, 'B: two')]
        lLintChecks = tool.extract_lint_checks(lWarningSection)
        self.assertEqual(['A', 'B'], [oLintCheck.sId for oLintCheck in lLintChecks])
        self.assertEqual([(3, 'A: one')], lLintChecks[0].lLines)
        self.assertEqual([(5, 'B: two')], lLintChecks[1].lLines)

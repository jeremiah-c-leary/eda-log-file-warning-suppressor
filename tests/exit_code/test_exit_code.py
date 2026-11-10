
import unittest

from elfws.exit_code import ExitCode


class test_exit_code(unittest.TestCase):

    def test_values_match_documentation(self):
        self.assertEqual(0, ExitCode.SUCCESS)
        self.assertEqual(1, ExitCode.SUPPRESSION_FILE_ERROR)
        self.assertEqual(2, ExitCode.NO_MATCHING_PARSER)
        self.assertEqual(3, ExitCode.NO_COMMAND_LINE_ARGUMENTS)
        self.assertEqual(4, ExitCode.REPORT_FILE_WRITE_ERROR)
        self.assertEqual(5, ExitCode.JUNIT_FILE_WRITE_ERROR)
        self.assertEqual(6, ExitCode.LOG_FILE_READ_ERROR)

    def test_every_exit_code_is_tested(self):
        self.assertEqual(7, len(ExitCode))

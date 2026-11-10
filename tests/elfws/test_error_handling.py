
import io
import unittest
from unittest import mock

from elfws import __main__
from elfws import error
from elfws.exit_code import ExitCode


class test_error_handling(unittest.TestCase):

    def test_error_carries_message_and_exit_code(self):
        oError = error.ElfwsError('something failed', ExitCode.LOG_FILE_READ_ERROR)
        self.assertEqual('something failed', str(oError))
        self.assertEqual(6, oError.iExitCode)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_error_message_is_printed_and_exit_code_returned(self, mock_stdout):
        with mock.patch('elfws.__main__.run', side_effect=error.ElfwsError('ERROR: broken', ExitCode.NO_MATCHING_PARSER)):
            iExitCode = __main__.run_and_report_errors()
        self.assertEqual(2, iExitCode)
        self.assertEqual('ERROR: broken\n', mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_error_without_message_prints_nothing(self, mock_stdout):
        with mock.patch('elfws.__main__.run', side_effect=error.ElfwsError('', ExitCode.NO_COMMAND_LINE_ARGUMENTS)):
            iExitCode = __main__.run_and_report_errors()
        self.assertEqual(3, iExitCode)
        self.assertEqual('', mock_stdout.getvalue())

    def test_subcommand_exit_code_is_returned(self):
        with mock.patch('elfws.__main__.run', return_value=ExitCode.SUCCESS):
            self.assertEqual(0, __main__.run_and_report_errors())

    def test_main_exits_with_the_exit_code(self):
        with mock.patch('elfws.__main__.run_and_report_errors', return_value=ExitCode.REPORT_FILE_WRITE_ERROR):
            with self.assertRaises(SystemExit) as oContext:
                __main__.main()
        self.assertEqual(4, oContext.exception.code)

    def test_other_exceptions_are_not_hidden(self):
        with mock.patch('elfws.__main__.run', side_effect=KeyError('bug')):
            with self.assertRaises(KeyError):
                __main__.run_and_report_errors()


import os
import tempfile
import unittest

from elfws import log_file
from elfws import error


class test_read_log_file(unittest.TestCase):

    def test_non_utf8_bytes_are_replaced(self):
        with tempfile.TemporaryDirectory() as sDir:
            sFile = os.path.join(sDir, 'latin1.log')
            with open(sFile, 'wb') as oFile:
                oFile.write(b'Microsemi Libero Software\nWarning: X: caf\xe9\n')
            lLines = log_file.read_log_file(sFile)
        self.assertEqual(['Microsemi Libero Software', 'Warning: X: caf�'], lLines)

    def test_windows_line_endings_are_stripped(self):
        with tempfile.TemporaryDirectory() as sDir:
            sFile = os.path.join(sDir, 'crlf.log')
            with open(sFile, 'wb') as oFile:
                oFile.write(b'line 1\r\nline 2\r\n')
            self.assertEqual(['line 1', 'line 2'], log_file.read_log_file(sFile))

    def test_missing_file_raises_log_file_read_error(self):
        with self.assertRaises(error.ElfwsError) as oContext:
            log_file.read_log_file('does/not/exist.log')
        self.assertEqual(6, oContext.exception.iExitCode)
        self.assertIn('ERROR: Could not read log file does/not/exist.log', str(oContext.exception))

    def test_directory_raises_log_file_read_error(self):
        with tempfile.TemporaryDirectory() as sDir:
            with self.assertRaises(error.ElfwsError) as oContext:
                log_file.read_log_file(sDir)
        self.assertEqual(6, oContext.exception.iExitCode)

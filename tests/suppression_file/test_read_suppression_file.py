
import os
import tempfile
import unittest

from elfws import suppression_file
from elfws import error


class test_read_suppression_file(unittest.TestCase):

    def setUp(self):
        self.oTempDir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.oTempDir.cleanup()

    def write_file(self, sName, bContent):
        sPath = os.path.join(self.oTempDir.name, sName)
        with open(sPath, 'wb') as oFile:
            oFile.write(bContent)
        return sPath

    def assert_raises_suppression_file_error(self, sPath):
        with self.assertRaises(error.ElfwsError) as oContext:
            suppression_file.read_suppression_file(sPath)
        self.assertEqual(oContext.exception.iExitCode, 1)

    def test_missing_file(self):
        self.assert_raises_suppression_file_error(os.path.join(self.oTempDir.name, 'missing.yaml'))

    def test_directory(self):
        self.assert_raises_suppression_file_error(self.oTempDir.name)

    def test_invalid_yaml(self):
        self.assert_raises_suppression_file_error(self.write_file('bad.yaml', b'suppress: [\n'))

    def test_non_utf8_file(self):
        self.assert_raises_suppression_file_error(self.write_file('latin1.yaml', b'suppress:\n  rules:\n    A:\n      - msg: caf\xe9\n'))

    def test_empty_file_returns_empty_dictionary(self):
        self.assertEqual({}, suppression_file.read_suppression_file(self.write_file('empty.yaml', b'')))

    def test_valid_file(self):
        sPath = self.write_file('ok.yaml', b'suppress:\n  rules:\n    A:\n      - msg: x\n')
        self.assertEqual({'suppress': {'rules': {'A': [{'msg': 'x'}]}}}, suppression_file.read_suppression_file(sPath))

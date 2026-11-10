
import io
import os
import sys
import tempfile
import unittest
from unittest import mock

from elfws import utils


sParserTemplate = '''
from elfws import warning
from elfws import warning_list


def get_vendor():
    return ['Test']


def get_tool_name():
    return '{name}'


def is_logfile(lFile):
    return lFile[0].startswith('{banner}')


def extract_warnings(lFile):
    oReturn = warning_list.WarningList()
    oReturn.add_warning(warning.LogWarning('{name}', 'parsed by {name}', None, 1))
    return oReturn
'''


def write_file(sPath, sContent):
    os.makedirs(os.path.dirname(sPath), exist_ok=True)
    with open(sPath, 'w') as oFile:
        oFile.write(sContent)


class test_parser_loading(unittest.TestCase):

    def setUp(self):
        self.oTempDir = tempfile.TemporaryDirectory()
        self.sVendorDir = self.oTempDir.name

    def tearDown(self):
        self.oTempDir.cleanup()

    def test_get_tools_only_returns_python_files(self):
        sToolDir = os.path.join(self.sVendorDir, 'test_vendor')
        write_file(os.path.join(sToolDir, 'parser.py'), '')
        write_file(os.path.join(sToolDir, 'README.md'), '')
        write_file(os.path.join(sToolDir, 'parser.py~'), '')
        write_file(os.path.join(sToolDir, 'notes.txt'), '')
        write_file(os.path.join(sToolDir, 'subdir.py', 'x.py'), '')
        lActual = [os.path.basename(s) for s in utils.get_tools(sToolDir)]
        self.assertEqual(['parser'], lActual)

    def test_user_defined_parser_overrides_built_in_parser(self):
        write_file(os.path.join(self.sVendorDir, 'test_vendor', 'user_designer.py'),
                   sParserTemplate.format(name='user_designer', banner='Microsemi Libero Software'))
        with mock.patch.dict(os.environ, {'ELFWS_USER_VENDOR_DIR': self.sVendorDir}):
            mTool = utils.get_vendor_tool_module(['Microsemi Libero Software'])
            self.assertEqual('user_designer', mTool.get_tool_name())
            oWarnList = utils.create_warning_list(['Microsemi Libero Software'], 'logfile')
            self.assertEqual('user_designer', oWarnList.get_warnings()[0].get_id())

    def test_built_in_parser_used_when_no_user_parser_matches(self):
        write_file(os.path.join(self.sVendorDir, 'test_vendor', 'other.py'),
                   sParserTemplate.format(name='other', banner='Something Else'))
        with mock.patch.dict(os.environ, {'ELFWS_USER_VENDOR_DIR': self.sVendorDir}):
            mTool = utils.get_vendor_tool_module(['Microsemi Libero Software'])
            self.assertEqual('designer', mTool.get_tool_name())

    @mock.patch('sys.stderr', new_callable=io.StringIO)
    def test_broken_parser_is_skipped_with_warning(self, mock_stderr):
        sBroken = os.path.join(self.sVendorDir, 'a_vendor', 'broken.py')
        write_file(sBroken, 'this is not python\n')
        write_file(os.path.join(self.sVendorDir, 'b_vendor', 'good.py'),
                   sParserTemplate.format(name='good', banner='Good Log'))
        with mock.patch.dict(os.environ, {'ELFWS_USER_VENDOR_DIR': self.sVendorDir}):
            mTool = utils.get_vendor_tool_module(['Good Log'])
        self.assertEqual('good', mTool.get_tool_name())
        self.assertIn('Could not load parser', mock_stderr.getvalue())
        self.assertIn(sBroken, mock_stderr.getvalue())

    def test_parsers_are_registered_under_unique_module_names(self):
        sToolA = os.path.join(self.sVendorDir, 'vendor_a', 'tool')
        sToolB = os.path.join(self.sVendorDir, 'vendor_b', 'tool')
        write_file(sToolA + '.py', sParserTemplate.format(name='a', banner='A'))
        write_file(sToolB + '.py', sParserTemplate.format(name='b', banner='B'))
        mToolA = utils.import_vendor_module(sToolA)
        mToolB = utils.import_vendor_module(sToolB)
        self.assertNotEqual(mToolA.__name__, mToolB.__name__)
        self.assertIs(sys.modules[mToolA.__name__], mToolA)
        self.assertIs(sys.modules[mToolB.__name__], mToolB)
        self.assertEqual('a', mToolA.get_tool_name())
        self.assertEqual('b', mToolB.get_tool_name())

    def test_parser_modules_are_cached(self):
        sTool = os.path.join(self.sVendorDir, 'vendor_a', 'tool')
        write_file(sTool + '.py', sParserTemplate.format(name='a', banner='A'))
        self.assertIs(utils.import_vendor_module(sTool), utils.import_vendor_module(sTool))



import unittest
from unittest import mock

from elfws import cmd_line_args

class testCmdLineArgsModule(unittest.TestCase):

    def test_is_dash_h_present(self):
        self.assertTrue(cmd_line_args.is_dash_h_present(['-h', '-home', 'noth']))
        self.assertTrue(cmd_line_args.is_dash_h_present(['-home', '-h', 'noth']))
        self.assertTrue(cmd_line_args.is_dash_h_present(['-home', 'noth', '-h']))
        self.assertFalse(cmd_line_args.is_dash_h_present(['-home', 'noth', '-house']))

        self.assertTrue(cmd_line_args.is_dash_h_present(['--help', '--home', 'noth']))
        self.assertTrue(cmd_line_args.is_dash_h_present(['--home', '--help', 'noth']))
        self.assertTrue(cmd_line_args.is_dash_h_present(['--home', 'noth', '--help']))
        self.assertFalse(cmd_line_args.is_dash_h_present(['--home', 'noth', '--house']))

    def test_remove_help_argument(self):
        lExpected = ['one', 'two']
        self.assertEqual(lExpected, cmd_line_args.remove_help_argument(['-h', 'one', 'two']))
        self.assertEqual(lExpected, cmd_line_args.remove_help_argument(['one', '-h', 'two']))
        self.assertEqual(lExpected, cmd_line_args.remove_help_argument(['one', 'two', '-h']))

        self.assertEqual(lExpected, cmd_line_args.remove_help_argument(['--help', 'one', 'two']))
        self.assertEqual(lExpected, cmd_line_args.remove_help_argument(['one', '--help', 'two']))
        self.assertEqual(lExpected, cmd_line_args.remove_help_argument(['one', 'two', '--help']))

    def test_extract_vendor_from_args(self):
        self.assertEqual('vendor', cmd_line_args.extract_vendor_from_args(['bin', 'cmd', 'vendor']))
        self.assertEqual('vendor', cmd_line_args.extract_vendor_from_args(['-h', 'bin', 'cmd', 'vendor']))
        self.assertEqual('vendor', cmd_line_args.extract_vendor_from_args(['bin', '-h', 'cmd', 'vendor']))
        self.assertEqual('vendor', cmd_line_args.extract_vendor_from_args(['bin', 'cmd', '-h', 'vendor']))
        self.assertEqual('vendor', cmd_line_args.extract_vendor_from_args(['bin', 'cmd', 'vendor', '-h']))
        self.assertEqual(None, cmd_line_args.extract_vendor_from_args(['bin']))
        self.assertEqual(None, cmd_line_args.extract_vendor_from_args(['bin', 'cmd']))
        self.assertEqual(None, cmd_line_args.extract_vendor_from_args(['bin', 'cmd', '-h']))

    def test_get_vendors(self):
        lExpected = ['microsemi']
        self.assertEqual(lExpected, cmd_line_args.get_vendors())

    def test_get_tools(self):
        lExpected = ['designer']
        self.assertEqual(lExpected, cmd_line_args.get_tools('microsemi'))

    def test_remove_extension(self):
        self.assertEqual('filename', cmd_line_args.remove_extension('filename.ext'))
        self.assertEqual('filename.blue', cmd_line_args.remove_extension('filename.blue.ext'))

    @mock.patch('sys.stdout')
    @mock.patch('sys.argv', ['elfws'])
    def test_parse_command_line_arguments_w_no_args(self, mockStdout):
        try:
            cmd_line_args.parse_command_line_arguments()
        except SystemExit:
            pass

        sOutput = 'usage: elfws [-h] {suppress,version} ...\n'
        sOutput += '\n'
        sOutput += 'Suppresses Warnings in logfiles.\n'
        sOutput += '\n'
        sOutput += 'positional arguments:\n'
        sOutput += '  {suppress,version}\n'
        sOutput += '    suppress          Suppress warnings\n'
        sOutput += '    version           Displays ELFWS version information\n'
        sOutput += '\n'
        sOutput += 'optional arguments:\n'
        sOutput += '  -h, --help          show this help message and exit\n'

        mockStdout.write.assert_has_calls([
            mock.call(sOutput)
        ])
        
    @mock.patch('sys.stdout')
    @mock.patch('sys.argv', ['elfws', 'suppress'])
    def test_parse_command_line_arguments_w_suppress_only(self, mockStdout):
        try:
            cmd_line_args.parse_command_line_arguments()
        except SystemExit:
            pass

        sOutput = 'usage: elfws suppress [-h] vendor tool log_file suppression_file\n'
        sOutput += '\n'
        sOutput += 'positional arguments:\n'
        sOutput += '  vendor            microsemi\n'
        sOutput += '  tool              Vendor tool\n'
        sOutput += '  log_file          Log file which will be checked for warnings\n'
        sOutput += '  suppression_file  Suppression file\n'
        sOutput += '\n'
        sOutput += 'optional arguments:\n'
        sOutput += '  -h, --help        show this help message and exit\n'

        mockStdout.write.assert_has_calls([
            mock.call(sOutput)
        ])

    @mock.patch('sys.stdout')
    @mock.patch('sys.argv', ['elfws', 'suppress', '-h'])
    def test_parse_command_line_arguments_w_suppress_only_w_dash_h(self, mockStdout):
        try:
            cmd_line_args.parse_command_line_arguments()
        except SystemExit:
            pass

        sOutput = 'usage: elfws suppress [-h] vendor tool log_file suppression_file\n'
        sOutput += '\n'
        sOutput += 'positional arguments:\n'
        sOutput += '  vendor            microsemi\n'
        sOutput += '  tool              Vendor tool\n'
        sOutput += '  log_file          Log file which will be checked for warnings\n'
        sOutput += '  suppression_file  Suppression file\n'
        sOutput += '\n'
        sOutput += 'optional arguments:\n'
        sOutput += '  -h, --help        show this help message and exit\n'

        mockStdout.write.assert_has_calls([
            mock.call(sOutput)
        ])

    @mock.patch('sys.stdout')
    @mock.patch('sys.argv', ['elfws', 'suppress', 'microsemi'])
    def test_parse_command_line_arguments_w_suppress_w_microsemi(self, mockStdout):
        try:
            cmd_line_args.parse_command_line_arguments()
        except SystemExit:
            pass

        sOutput = 'usage: elfws suppress [-h] vendor tool log_file suppression_file\n'
        sOutput += '\n'
        sOutput += 'positional arguments:\n'
        sOutput += '  vendor            microsemi\n'
        sOutput += '  tool              designer\n'
        sOutput += '  log_file          Log file which will be checked for warnings\n'
        sOutput += '  suppression_file  Suppression file\n'
        sOutput += '\n'
        sOutput += 'optional arguments:\n'
        sOutput += '  -h, --help        show this help message and exit\n'

        mockStdout.write.assert_has_calls([
            mock.call(sOutput)
        ])

    @mock.patch('sys.stdout')
    @mock.patch('sys.argv', ['elfws', 'suppress', 'microsemi', '-h'])
    def test_parse_command_line_arguments_w_suppress_w_microsemi_w_dash_h(self, mockStdout):
        try:
            cmd_line_args.parse_command_line_arguments()
        except SystemExit:
            pass

        sOutput = 'usage: elfws suppress [-h] vendor tool log_file suppression_file\n'
        sOutput += '\n'
        sOutput += 'positional arguments:\n'
        sOutput += '  vendor            microsemi\n'
        sOutput += '  tool              designer\n'
        sOutput += '  log_file          Log file which will be checked for warnings\n'
        sOutput += '  suppression_file  Suppression file\n'
        sOutput += '\n'
        sOutput += 'optional arguments:\n'
        sOutput += '  -h, --help        show this help message and exit\n'

        mockStdout.write.assert_has_calls([
            mock.call(sOutput)
        ])

    @mock.patch('sys.stdout')
    @mock.patch('sys.argv', ['elfws', 'suppress', 'microsemi', 'designer'])
    def test_parse_command_line_arguments_w_suppress_w_microsemi_w_designer(self, mockStdout):
        try:
            cmd_line_args.parse_command_line_arguments()
        except SystemExit:
            pass

        sOutput = 'usage: elfws suppress [-h] vendor tool log_file suppression_file\n'
        sOutput += '\n'
        sOutput += 'positional arguments:\n'
        sOutput += '  vendor            microsemi\n'
        sOutput += '  tool              designer\n'
        sOutput += '  log_file          Log file which will be checked for warnings\n'
        sOutput += '  suppression_file  Suppression file\n'
        sOutput += '\n'
        sOutput += 'optional arguments:\n'
        sOutput += '  -h, --help        show this help message and exit\n'

        mockStdout.write.assert_has_calls([
            mock.call(sOutput)
        ])

    @mock.patch('sys.stdout')
    @mock.patch('sys.argv', ['elfws', 'suppress', 'microsemi', 'designer', '-h'])
    def test_parse_command_line_arguments_w_suppress_w_microsemi_w_designer_w_dash_h(self, mockStdout):
        try:
            cmd_line_args.parse_command_line_arguments()
        except SystemExit:
            pass

        sOutput = 'usage: elfws suppress [-h] vendor tool log_file suppression_file\n'
        sOutput += '\n'
        sOutput += 'positional arguments:\n'
        sOutput += '  vendor            microsemi\n'
        sOutput += '  tool              designer\n'
        sOutput += '  log_file          Log file which will be checked for warnings\n'
        sOutput += '  suppression_file  Suppression file\n'
        sOutput += '\n'
        sOutput += 'optional arguments:\n'
        sOutput += '  -h, --help        show this help message and exit\n'

        mockStdout.write.assert_has_calls([
            mock.call(sOutput)
        ])

    @mock.patch('sys.stdout')
    @mock.patch('sys.argv', ['elfws', 'suppress', 'microsemi', 'designer', 'logFile'])
    def test_parse_command_line_arguments_w_suppress_w_microsemi_w_designer_w_logfile(self, mockStdout):
        try:
            cmd_line_args.parse_command_line_arguments()
        except SystemExit:
            pass

        sOutput = 'usage: elfws suppress [-h] vendor tool log_file suppression_file\n'
        sOutput += '\n'
        sOutput += 'positional arguments:\n'
        sOutput += '  vendor            microsemi\n'
        sOutput += '  tool              designer\n'
        sOutput += '  log_file          Log file which will be checked for warnings\n'
        sOutput += '  suppression_file  Suppression file\n'
        sOutput += '\n'
        sOutput += 'optional arguments:\n'
        sOutput += '  -h, --help        show this help message and exit\n'

        mockStdout.write.assert_has_calls([
            mock.call(sOutput)
        ])

    @mock.patch('sys.stdout')
    @mock.patch('sys.argv', ['elfws', 'suppress', 'microsemi', 'designer', 'logFile', '-h'])
    def test_parse_command_line_arguments_w_suppress_w_microsemi_w_designer_w_logfile_w_dash_h(self, mockStdout):
        try:
            cmd_line_args.parse_command_line_arguments()
        except SystemExit:
            pass

        sOutput = 'usage: elfws suppress [-h] vendor tool log_file suppression_file\n'
        sOutput += '\n'
        sOutput += 'positional arguments:\n'
        sOutput += '  vendor            microsemi\n'
        sOutput += '  tool              designer\n'
        sOutput += '  log_file          Log file which will be checked for warnings\n'
        sOutput += '  suppression_file  Suppression file\n'
        sOutput += '\n'
        sOutput += 'optional arguments:\n'
        sOutput += '  -h, --help        show this help message and exit\n'

        mockStdout.write.assert_has_calls([
            mock.call(sOutput)
        ])

    @mock.patch('sys.stdout')
    @mock.patch('sys.argv', ['elfws', 'suppress', 'invalid'])
    def test_parse_command_line_arguments_w_suppress_w_invalid_vendor(self, mockStdout):
        try:
            cmd_line_args.parse_command_line_arguments()
        except SystemExit:
            pass

        sOutput = 'usage: elfws suppress [-h] vendor tool log_file suppression_file\n'
        sOutput += '\n'
        sOutput += 'positional arguments:\n'
        sOutput += '  vendor            microsemi\n'
        sOutput += '  tool              Vendor tool\n'
        sOutput += '  log_file          Log file which will be checked for warnings\n'
        sOutput += '  suppression_file  Suppression file\n'
        sOutput += '\n'
        sOutput += 'optional arguments:\n'
        sOutput += '  -h, --help        show this help message and exit\n'

        mockStdout.write.assert_has_calls([
            mock.call(sOutput)
        ])

    @mock.patch('sys.stdout')
    @mock.patch('sys.argv', ['elfws', 'suppress', 'invalid', '-h'])
    def test_parse_command_line_arguments_w_suppress_w_invalid_vendor_w_dash_h(self, mockStdout):
        try:
            cmd_line_args.parse_command_line_arguments()
        except SystemExit:
            pass

        sOutput = 'usage: elfws suppress [-h] vendor tool log_file suppression_file\n'
        sOutput += '\n'
        sOutput += 'positional arguments:\n'
        sOutput += '  vendor            microsemi\n'
        sOutput += '  tool              Vendor tool\n'
        sOutput += '  log_file          Log file which will be checked for warnings\n'
        sOutput += '  suppression_file  Suppression file\n'
        sOutput += '\n'
        sOutput += 'optional arguments:\n'
        sOutput += '  -h, --help        show this help message and exit\n'

        mockStdout.write.assert_has_calls([
            mock.call(sOutput)
        ])

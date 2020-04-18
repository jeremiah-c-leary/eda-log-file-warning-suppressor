

import unittest
from unittest import mock

from elfws import cmd_line_args

class testCmdLineArgsModule(unittest.TestCase):

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
        sOutput += '    suppress          Suppresses warnings in logfiles\n'
        sOutput += '    version           Displays ELFWS version information\n'
        sOutput += '\n'
        sOutput += 'optional arguments:\n'
        sOutput += '  -h, --help          show this help message and exit\n'

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

        sOutput = 'usage: elfws suppress [-h] log_file suppression_file\n'
        sOutput += '\n'
        sOutput += 'positional arguments:\n'
        sOutput += '  log_file          Log file to check for warnings\n'
        sOutput += '  suppression_file  YAML formatted warning suppression file\n'
        sOutput += '\n'
        sOutput += 'optional arguments:\n'
        sOutput += '  -h, --help        show this help message and exit\n'

        mockStdout.write.assert_has_calls([
            mock.call(sOutput)
        ])

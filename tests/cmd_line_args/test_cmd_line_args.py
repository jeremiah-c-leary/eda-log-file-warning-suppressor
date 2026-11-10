

import unittest
from unittest import mock

from elfws import cmd_line_args
from elfws import subcommand

class testCmdLineArgsModule(unittest.TestCase):

    @mock.patch('sys.stdout')
    @mock.patch('sys.argv', ['elfws'])
    def test_parse_command_line_arguments_w_no_args(self, mockStdout):
        with self.assertRaises(SystemExit) as oContext:
            cmd_line_args.parse_command_line_arguments()

        self.assertEqual(oContext.exception.code, 3)

        sOutput = 'usage: elfws [-h] {create,report,show,suppress,version} ...\n'
        sOutput += '\n'
        sOutput += 'Suppresses Warnings in logfiles.\n'
        sOutput += '\n'
        sOutput += 'positional arguments:\n'
        sOutput += '  {create,report,show,suppress,version}\n'
        sOutput += '    create              Create suppression file\n'
        sOutput += '    report              Generate an audit report\n'
        sOutput += '    show                Show warnings in logfiles\n'
        sOutput += '    suppress            Suppresses warnings in logfiles\n'
        sOutput += '    version             Displays ELFWS version information\n'
        sOutput += '\n'
        sOutput += 'options:\n'
        sOutput += '  -h, --help            show this help message and exit\n'

        mockStdout.write.assert_has_calls([
            mock.call(sOutput)
        ])
        
    @mock.patch('sys.stdout')
    @mock.patch('sys.argv', ['elfws', 'suppress', '-h'])
    def test_parse_command_line_arguments_w_suppress_only_w_dash_h(self, mockStdout):
        with self.assertRaises(SystemExit) as oContext:
            cmd_line_args.parse_command_line_arguments()

        self.assertEqual(oContext.exception.code, 0)

        sOutput = 'usage: elfws suppress [-h] log_file suppression_file\n'
        sOutput += '\n'
        sOutput += 'positional arguments:\n'
        sOutput += '  log_file          Log file to check for warnings\n'
        sOutput += '  suppression_file  YAML formatted warning suppression file\n'
        sOutput += '\n'
        sOutput += 'options:\n'
        sOutput += '  -h, --help        show this help message and exit\n'

        mockStdout.write.assert_has_calls([
            mock.call(sOutput)
        ])

    def test_each_subcommand_dispatches_to_its_function(self):
        dExpected = {
            'create': (['create', 'log', 'out.yaml'], subcommand.create.create),
            'report': (['report', 'log', 'sup.yaml', 'report.rpt'], subcommand.report.report),
            'show': (['show', 'log'], subcommand.show.show),
            'suppress': (['suppress', 'log', 'sup.yaml'], subcommand.suppress.suppress),
            'version': (['version'], subcommand.version.print_version),
        }
        for sName, (lArgs, fExpected) in dExpected.items():
            with self.subTest(subcommand=sName):
                with mock.patch('sys.argv', ['elfws'] + lArgs):
                    oCommandLineArguments = cmd_line_args.parse_command_line_arguments()
                self.assertIs(fExpected, oCommandLineArguments.run_subcommand)

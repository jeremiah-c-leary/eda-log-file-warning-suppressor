

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

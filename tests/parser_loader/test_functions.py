
import os
import unittest

from elfws import parser_loader
from elfws import error


class test_functions(unittest.TestCase):

    def test_get_vendors(self):
        lActual = parser_loader.get_vendors('elfws/vendor')
        self.assertEqual(4, len(lActual))
        self.assertTrue('elfws/vendor/mentor_graphics' in lActual) 
        self.assertTrue('elfws/vendor/microsemi' in lActual) 
        self.assertTrue('elfws/vendor/synopsys' in lActual) 
        self.assertTrue('elfws/vendor/xilinx' in lActual) 

    def test_get_tools(self):
        lExpected = ['designer']
        lActual = [os.path.basename(s) for s in parser_loader.get_tools('elfws/vendor/microsemi')]
        self.assertEqual(sorted(lExpected), sorted(lActual))
        lExpected = ['questa_cdc__cdc_run_log', 'questa_cdc__cdc_detail_rpt', 'precision', 'questa_lint']
        lActual = [os.path.basename(s) for s in parser_loader.get_tools('elfws/vendor/mentor_graphics')]
        self.assertEqual(sorted(lExpected), sorted(lActual))

    def test_remove_extension(self):
        self.assertEqual('filename', parser_loader.remove_extension('filename.ext'))
        self.assertEqual('filename.blue', parser_loader.remove_extension('filename.blue.ext'))

    def test_get_vendor_tool_module(self):
        lLogFile = []
        lLogFile.append('Microsemi Libero Software')

        mTool = parser_loader.get_vendor_tool_module(lLogFile)
        self.assertEqual('designer', mTool.get_tool_name())
        self.assertEqual(['Actel', 'Microsemi'], mTool.get_vendor())

        lLogFile = []
        lLogFile.append('icrosemi Libero Software')

        mTool = parser_loader.get_vendor_tool_module(lLogFile)
        self.assertEqual(None, mTool)

    def test_create_warning_list(self):
        with self.assertRaises(error.ElfwsError) as oContext:
            parser_loader.create_warning_list(['Not a log file'], 'logfile_name')

        self.assertEqual(oContext.exception.iExitCode, 2)
        self.assertEqual('ERROR: File logfile_name is not recognized as a supported logfile.', str(oContext.exception))

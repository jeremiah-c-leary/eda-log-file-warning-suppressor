
import importlib
import os
import unittest
from unittest import mock

from elfws import utils
from elfws import suppression_list
from elfws import suppression


class test_functions(unittest.TestCase):

    def test_build_vendor_module_path(self):
        self.assertEqual('elfws.vendor.microsemi.designer', utils.build_vendor_module_path('microsemi', 'designer'))
        self.assertEqual('elfws.vendor.vendorname.toolname', utils.build_vendor_module_path('vendorName', 'toolName'))


    def test_read_suppression_file(self):
        dExpected = {}
        dExpected['suppress'] = {}

        dExpected['suppress']['rules'] = {}

        dExpected['suppress']['rules']['SYN001'] = []
        dRule = {}
        dRule['msg'] = 'This is the message'
        dRule['author'] = 'jcleary'
        dRule['comment'] = 'This is fine because...'
        dRule['error'] = 'This should not be picked up'
        dExpected['suppress']['rules']['SYN001'].append(dRule)
        dRule = {}
        dRule['msg'] = 'This is another message'
        dRule['comment'] = 'Just ignore this...'
        dExpected['suppress']['rules']['SYN001'].append(dRule)

        dExpected['suppress']['rules']['NO_ID'] = []
        dRule = {}
        dRule['msg'] = 'Some warning without a proper ID'
        dRule['comment'] = 'This is fine...'
        dExpected['suppress']['rules']['NO_ID'].append(dRule)

        dExpected['suppress']['rules']['CMP2001'] = []
        dRule = {}
        dRule['msg'] = 'This is some compile warning'
        dRule['author'] = 'jcleary'
        dRule['comment'] = 'Just because...'
        dExpected['suppress']['rules']['CMP2001'].append(dRule)
        
        dActual = utils.read_suppression_file(os.path.join(os.path.dirname(__file__),'suppress.yaml'))
        self.assertEqual(dExpected, dActual)

    def test_read_suppression_file_w_empty_file(self):
        dExpected = {}

        dActual = utils.read_suppression_file(os.path.join(os.path.dirname(__file__),'empty_suppress.yaml'))

        self.assertEqual(dExpected, dActual)

    def test_create_suppression_list(self):

        dSuppression = {}
        dSuppression['suppress'] = {}
        dSuppression['suppress']['rules'] = {}

        dSuppression['suppress']['rules']['SYN001'] = []
        dRule = {}
        dRule['msg'] = 'This is the message'
        dRule['author'] = 'jcleary'
        dRule['comment'] = 'This is fine because...'
        dSuppression['suppress']['rules']['SYN001'].append(dRule)
        dRule = {}
        dRule['msg'] = 'This is another message'
        dRule['comment'] = 'Just ignore this...'
        dSuppression['suppress']['rules']['SYN001'].append(dRule)

        dSuppression['suppress']['rules']['NO_ID'] = []
        dRule = {}
        dRule['msg'] = 'Some warning without a proper ID'
        dRule['comment'] = 'This is fine...'
        dSuppression['suppress']['rules']['NO_ID'].append(dRule)

        dSuppression['suppress']['rules']['CMP2001'] = []
        dRule = {}
        dRule['msg'] = 'This is some compile warning'
        dRule['author'] = 'jcleary'
        dRule['comment'] = 'Just because...'
        dSuppression['suppress']['rules']['CMP2001'].append(dRule)
        
        dSuppression['suppress']['rules']['NO_COMMENT'] = []
        dRule = {}
        dRule['msg'] = 'This rule has no comment'
        dSuppression['suppress']['rules']['NO_COMMENT'].append(dRule)

        oActualSuppressionList = utils.create_suppression_list(dSuppression)

        oExpectedSuppressList = suppression_list.create()

        oSuppression = suppression.create('SYN001', 'This is the message', 'jcleary', 'This is fine because...')
        oExpectedSuppressList.suppressions.append(oSuppression)
        
        oSuppression = suppression.create('SYN001', 'This is another message', '<None>', 'Just ignore this...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.create('NO_ID', 'Some warning without a proper ID', '<None>', 'This is fine...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.create('CMP2001', 'This is some compile warning', 'jcleary', 'Just because...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.create('NO_COMMENT', 'This rule has no comment', '<None>', '<None>')

        self.assertEqual(5, len(oActualSuppressionList.suppressions))
        oExpectedSuppressList.suppressions.append(oSuppression)

        for i in range(5):
            oExpected = oExpectedSuppressList.suppressions[i]
            oActual = oActualSuppressionList.suppressions[i]

            self.assertEqual(oExpected.get_warning_id(), oActual.get_warning_id())
            self.assertEqual(oExpected.get_message(), oActual.get_message())
            self.assertEqual(oExpected.get_author(), oActual.get_author())
            self.assertEqual(oExpected.get_comment(), oActual.get_comment())
            self.assertEqual(oExpected.get_investigate(), oActual.get_investigate())

    def test_create_suppression_list_w_empty_dictionary(self):
        dSuppression = {}
        oActualSuppressionList = utils.create_suppression_list(dSuppression)
        oExpectedSuppressionList = suppression_list.create()

        self.assertEqual(0, len(oActualSuppressionList.suppressions))

    def test_create_suppression_list_w_groupings(self):

        dSuppression = utils.read_suppression_file(os.path.join(os.path.dirname(__file__),'suppress_w_groupings.yaml'))

        oActualSuppressionList = utils.create_suppression_list(dSuppression)

        oExpectedSuppressList = suppression_list.create()

        oSuppression = suppression.create('SYN001', 'This is the message', 'jcleary', 'This is fine because...')
        oExpectedSuppressList.suppressions.append(oSuppression)
        
        oSuppression = suppression.create('SYN001', 'This is another message', '<None>', 'Just ignore this...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.create('NO_ID', 'Some warning without a proper ID', '<None>', 'This is fine...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.create('CMP2001', 'This is some compile warning', 'jcleary', 'Just because...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.create('NO_ID', 'Top level message', '<None>', 'should be parsed as a warning.')

        self.assertEqual(5, len(oActualSuppressionList.suppressions))
        oExpectedSuppressList.suppressions.append(oSuppression)

        for i in range(5):
            oExpected = oExpectedSuppressList.suppressions[i]
            oActual = oActualSuppressionList.suppressions[i]
            self.assertEqual(oExpected.get_warning_id(), oActual.get_warning_id())
            self.assertEqual(oExpected.get_message(), oActual.get_message())
            self.assertEqual(oExpected.get_author(), oActual.get_author())
            self.assertEqual(oExpected.get_comment(), oActual.get_comment())
            self.assertEqual(oExpected.get_investigate(), oActual.get_investigate())

    def test_create_suppression_list_w_investigates(self):

        dSuppression = utils.read_suppression_file(os.path.join(os.path.dirname(__file__),'investigate_suppress.yaml'))

        oActualSuppressionList = utils.create_suppression_list(dSuppression)

        oExpectedSuppressList = suppression_list.create()

        oSuppression = suppression.create('SYN001', 'This is the message', 'jcleary', 'This is fine because...')
        oExpectedSuppressList.suppressions.append(oSuppression)
        
        oSuppression = suppression.create('SYN001', 'This is another message', '<None>', 'Just ignore this...')
        oSuppression.investigate = True
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.create('NO_ID', 'Some warning without a proper ID', '<None>', 'This is fine...')
        oSuppression.investigate = True
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.create('NO_ID', 'This is another NO_ID suppression rule', '<None>', 'Both this and the other NO_ID must be present.')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.create('CMP2001', 'This is some compile warning', 'jcleary', 'Just because...')
        oSuppression.investigate = True
        oExpectedSuppressList.suppressions.append(oSuppression)


        self.assertEqual(5, len(oActualSuppressionList.suppressions))
        oExpectedSuppressList.suppressions.append(oSuppression)

        for i in range(5):
            oExpected = oExpectedSuppressList.suppressions[i]
            oActual = oActualSuppressionList.suppressions[i]

            self.assertEqual(oExpected.get_warning_id(), oActual.get_warning_id())
            self.assertEqual(oExpected.get_message(), oActual.get_message())
            self.assertEqual(oExpected.get_author(), oActual.get_author())
            self.assertEqual(oExpected.get_comment(), oActual.get_comment())
            self.assertEqual(oExpected.get_investigate(), oActual.get_investigate())

    def test_read_log_file(self):
        lExpected = []
        lExpected.append('Microsemi Libero Software')
        lExpected.append('Version: 11.9.2.1')
        lExpected.append('Release: 11.9 SP2')
        lExpected.append('')
        lExpected.append('Created a new design.')
        lExpected.append('')
        lExpected.append('# This is a warning with an ID')
        lExpected.append('Warning: DEF1234 : This is a warning')
        lExpected.append('')
        lExpected.append('# This is a warning without an ID')
        lExpected.append('Warning: This is a warning without an ID')
        lExpected.append('Warning: This is a warning with a : that does not have an ID')
        lExpected.append('')
        lExpected.append('# This is a multiline warning with an ID')
        lExpected.append('Warning: MULTI546 : This is the first line of the warning')
        lExpected.append('         This is the second line of the warning')
        lExpected.append(' This is the last line of the warning.')
        lExpected.append('')
        lExpected.append('# This is a multiline warning without an ID')
        lExpected.append('Warning: This is the first line : of the message')
        lExpected.append(' This is the second line of the message')
        lExpected.append('   This is the third line of the message')
        lExpected.append('  This is the last line of the message.')
        lExpected.append('')
        lExpected.append('#These should not be counted as warnings:')
        lExpected.append(' Warning: ABC5425 : this is not a warning because of the leading space')
        lExpected.append('')
        lExpected.append('')

        self.assertEqual(lExpected, utils.read_log_file('tests/vendor/microsemi/designer/warning_messages.log'))

    def test_import_vendor_module(self):
        self.assertEqual(importlib.import_module('elfws.vendor.microsemi.designer'), utils.import_vendor_module('microsemi', 'designer'))

    def test_get_vendors(self):
        lExpected = ['mentor_graphics', 'microsemi', 'xilinx']
        self.assertEqual(lExpected, utils.get_vendors())

    def test_get_tools(self):
        lExpected = ['designer']
        self.assertEqual(lExpected, utils.get_tools('microsemi'))

    def test_remove_extension(self):
        self.assertEqual('filename', utils.remove_extension('filename.ext'))
        self.assertEqual('filename.blue', utils.remove_extension('filename.blue.ext'))

    def test_get_vendor_tool_module(self):
        lLogFile = []
        lLogFile.append('Microsemi Libero Software')

        mTool = utils.get_vendor_tool_module(lLogFile)
        self.assertEqual('designer', mTool.get_tool_name())
        self.assertEqual(['Actel', 'Microsemi'], mTool.get_vendor())

        lLogFile = []
        lLogFile.append('icrosemi Libero Software')

        mTool = utils.get_vendor_tool_module(lLogFile)
        self.assertEqual(None, mTool)

    @mock.patch('sys.stdout')
    def test_create_warning_list(self, mock_stdout):
        try:
            utils.create_warning_list(['Not a log file'], 'logfile_name')
        except SystemExit:
            pass

        mock_stdout.write.assert_has_calls([
            mock.call('ERROR: File logfile_name is not recognized as a supported logfile.'), mock.call('\n')
        ])


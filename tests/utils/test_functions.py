
import importlib
import os
import unittest


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

        dExpected['suppress']['SYN001'] = []
        dRule = {}
        dRule['msg'] = 'This is the message'
        dRule['author'] = 'jcleary'
        dRule['comment'] = 'This is fine because...'
        dRule['error'] = 'This should not be picked up'
        dExpected['suppress']['SYN001'].append(dRule)
        dRule = {}
        dRule['msg'] = 'This is another message'
        dRule['comment'] = 'Just ignore this...'
        dExpected['suppress']['SYN001'].append(dRule)

        dExpected['suppress']['NO_ID'] = []
        dRule = {}
        dRule['msg'] = 'Some warning without a proper ID'
        dRule['comment'] = 'This is fine...'
        dExpected['suppress']['NO_ID'].append(dRule)

        dExpected['suppress']['CMP2001'] = []
        dRule = {}
        dRule['msg'] = 'This is some compile warning'
        dRule['author'] = 'jcleary'
        dRule['comment'] = 'Just because...'
        dExpected['suppress']['CMP2001'].append(dRule)
        
        dActual = utils.read_suppression_file(os.path.join(os.path.dirname(__file__),'suppress.yaml'))
        self.assertEqual(dExpected, dActual)

    def test_create_suppression_list(self):

        dSuppression = {}
        dSuppression['suppress'] = {}

        dSuppression['suppress']['SYN001'] = []
        dRule = {}
        dRule['msg'] = 'This is the message'
        dRule['author'] = 'jcleary'
        dRule['comment'] = 'This is fine because...'
        dSuppression['suppress']['SYN001'].append(dRule)
        dRule = {}
        dRule['msg'] = 'This is another message'
        dRule['comment'] = 'Just ignore this...'
        dSuppression['suppress']['SYN001'].append(dRule)

        dSuppression['suppress']['NO_ID'] = []
        dRule = {}
        dRule['msg'] = 'Some warning without a proper ID'
        dRule['comment'] = 'This is fine...'
        dSuppression['suppress']['NO_ID'].append(dRule)

        dSuppression['suppress']['CMP2001'] = []
        dRule = {}
        dRule['msg'] = 'This is some compile warning'
        dRule['author'] = 'jcleary'
        dRule['comment'] = 'Just because...'
        dSuppression['suppress']['CMP2001'].append(dRule)
        
        dSuppression['suppress']['NO_COMMENT'] = []
        dRule = {}
        dRule['msg'] = 'This rule has no comment'
        dSuppression['suppress']['NO_COMMENT'].append(dRule)

        oActualSuppressionList = utils.create_suppression_list(dSuppression)

        oExpectedSuppressList = suppression_list.create()

        oSuppression = suppression.create('SYN001', 'This is the message', 'jcleary', 'This is fine because...')
        oExpectedSuppressList.suppressions.append(oSuppression)
        
        oSuppression = suppression.create('SYN001', 'This is another message', None, 'Just ignore this...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.create('NO_ID', 'Some warning without a proper ID', None, 'This is fine...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.create('CMP2001', 'This is some compile warning', 'jcleary', 'Just because...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.create('NO_COMMENT', 'This rule has no comment')

        self.assertEqual(5, len(oActualSuppressionList.suppressions))
        oExpectedSuppressList.suppressions.append(oSuppression)

        for i in range(5):
            oExpected = oExpectedSuppressList.suppressions[i]
            oActual = oActualSuppressionList.suppressions[i]

            self.assertEqual(oExpected.get_warning_id(), oActual.get_warning_id())
            self.assertEqual(oExpected.get_message(), oActual.get_message())
            self.assertEqual(oExpected.get_author(), oActual.get_author())
            self.assertEqual(oExpected.get_comment(), oActual.get_comment())

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

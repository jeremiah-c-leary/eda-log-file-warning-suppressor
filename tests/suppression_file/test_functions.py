
import os
import unittest

from elfws import suppression
from elfws import suppression_file
from elfws import suppression_list
from elfws import error


class test_functions(unittest.TestCase):

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
        
        dActual = suppression_file.read_suppression_file(os.path.join(os.path.dirname(__file__),'suppress.yaml'))
        self.assertEqual(dExpected, dActual)

    def test_read_suppression_file_w_empty_file(self):
        dExpected = {}

        dActual = suppression_file.read_suppression_file(os.path.join(os.path.dirname(__file__),'empty_suppress.yaml'))

        self.assertEqual(dExpected, dActual)

    def test_read_suppression_file_w_error(self):
        with self.assertRaises(error.ElfwsError) as oContext:
            suppression_file.read_suppression_file(os.path.join(os.path.dirname(__file__),'error_suppress.yaml'))

        self.assertEqual(oContext.exception.iExitCode, 1)

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

        oActualSuppressionList = suppression_file.create_suppression_list(dSuppression)

        oExpectedSuppressList = suppression_list.SuppressionList()

        oSuppression = suppression.Suppression('SYN001', 'This is the message', 'jcleary', 'This is fine because...')
        oExpectedSuppressList.suppressions.append(oSuppression)
        
        oSuppression = suppression.Suppression('SYN001', 'This is another message', '<None>', 'Just ignore this...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.Suppression('NO_ID', 'Some warning without a proper ID', '<None>', 'This is fine...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.Suppression('CMP2001', 'This is some compile warning', 'jcleary', 'Just because...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.Suppression('NO_COMMENT', 'This rule has no comment', '<None>', '<None>')

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
        oActualSuppressionList = suppression_file.create_suppression_list(dSuppression)

        self.assertEqual(0, len(oActualSuppressionList.suppressions))

    def test_create_suppression_list_w_groupings(self):

        dSuppression = suppression_file.read_suppression_file(os.path.join(os.path.dirname(__file__),'suppress_w_groupings.yaml'))

        oActualSuppressionList = suppression_file.create_suppression_list(dSuppression)

        oExpectedSuppressList = suppression_list.SuppressionList()

        oSuppression = suppression.Suppression('SYN001', 'This is the message', 'jcleary', 'This is fine because...')
        oExpectedSuppressList.suppressions.append(oSuppression)
        
        oSuppression = suppression.Suppression('SYN001', 'This is another message', '<None>', 'Just ignore this...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.Suppression('NO_ID', 'Some warning without a proper ID', '<None>', 'This is fine...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.Suppression('CMP2001', 'This is some compile warning', 'jcleary', 'Just because...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.Suppression('NO_ID', 'Top level message', '<None>', 'should be parsed as a warning.')

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

        dSuppression = suppression_file.read_suppression_file(os.path.join(os.path.dirname(__file__),'investigate_suppress.yaml'))

        oActualSuppressionList = suppression_file.create_suppression_list(dSuppression)

        oExpectedSuppressList = suppression_list.SuppressionList()

        oSuppression = suppression.Suppression('SYN001', 'This is the message', 'jcleary', 'This is fine because...')
        oExpectedSuppressList.suppressions.append(oSuppression)
        
        oSuppression = suppression.Suppression('SYN001', 'This is another message', '<None>', 'Just ignore this...')
        oSuppression.investigate = True
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.Suppression('NO_ID', 'Some warning without a proper ID', '<None>', 'This is fine...')
        oSuppression.investigate = True
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.Suppression('NO_ID', 'This is another NO_ID suppression rule', '<None>', 'Both this and the other NO_ID must be present.')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.Suppression('CMP2001', 'This is some compile warning', 'jcleary', 'Just because...')
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

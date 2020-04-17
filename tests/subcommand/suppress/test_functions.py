
import os
import unittest


from elfws.subcommand import suppress
from elfws import suppression_list
from elfws import suppression


class test_functions(unittest.TestCase):

    def test_read_suppression_file(self):
        dExpected = {}
        dExpected['suppress'] = {}

        dExpected['suppress']['SYN001'] = []
        dRule = {}
        dRule['msg'] = 'This is the message'
        dRule['author'] = 'jcleary'
        dRule['comment'] = 'This is fine because...'
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
        
        dActual = suppress.read_suppression_file(os.path.join(os.path.dirname(__file__),'suppress.yaml'))
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

        oActualSuppressionList = suppress.create_suppression_list(dSuppression)

        oExpectedSuppressList = suppression_list.create()

        oSuppression = suppression.create('SYN001', 'This is the message', 'jcleary', 'This is fine because...')
        oExpectedSuppressList.suppressions.append(oSuppression)
        
        oSuppression = suppression.create('SYN001', 'This is another message', None, 'Just ignore this...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.create('NO_ID', 'Some warning without a proper ID', None, 'This is fine...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        oSuppression = suppression.create('CMP2001', 'This is some compile warning', 'jcleary', 'Just because...')
        oExpectedSuppressList.suppressions.append(oSuppression)

        self.assertEqual(4, len(oActualSuppressionList.suppressions))

        for i in range(4):
            oExpected = oExpectedSuppressList.suppressions[i]
            oActual = oActualSuppressionList.suppressions[i]

            self.assertEqual(oExpected.get_warning_id(), oActual.get_warning_id())
            self.assertEqual(oExpected.get_message(), oActual.get_message())
            self.assertEqual(oExpected.get_author(), oActual.get_author())
            self.assertEqual(oExpected.get_comment(), oActual.get_comment())


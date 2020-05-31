
import unittest

from elfws import suppression
from elfws import suppression_list

class testSuppressionListClassMethods(unittest.TestCase):

    def test_empty_suppression_list_creation(self):
        oSuppressionList = suppression_list.create()
        self.assertEqual([], oSuppressionList.suppressions)

    def test_add_suppression_method(self):
        oSuppressionList = suppression_list.create()

        oSuppressionList.add_suppression(suppression.create('WID1'))
        oSuppressionList.add_suppression(suppression.create('WID2'))

        self.assertEqual('WID1', oSuppressionList.suppressions[0].warning_id)
        self.assertEqual('WID2', oSuppressionList.suppressions[1].warning_id)

    def test_get_number_of_suppressions(self):

        oSuppressionList = suppression_list.create()

        self.assertEqual(0, oSuppressionList.get_number_of_suppressions())

        oSuppressionList.add_suppression(suppression.create('WID1'))

        self.assertEqual(1, oSuppressionList.get_number_of_suppressions())

        oSuppressionList.add_suppression(suppression.create('WID2'))

        self.assertEqual(2, oSuppressionList.get_number_of_suppressions())

    def test_get_suppressions_which_suppressed_a_warning(self):

        oSuppressionList = suppression_list.create()

        oSuppression = suppression.create()
        oSuppression.add_suppressed_warning('Hello')
        oSuppression.add_suppressed_warning('Hello 2')
        oSuppressionList.add_suppression(oSuppression)

        oSuppression = suppression.create()
        oSuppression.add_suppressed_warning('Goodbye')
        oSuppressionList.add_suppression(oSuppression)

        oSuppression = suppression.create()
        oSuppressionList.add_suppression(oSuppression)

        lActual = oSuppressionList.get_suppressions_which_suppressed_a_warning()

        self.assertEqual(2, len(lActual))

        self.assertEqual('Hello', lActual[0].get_suppressed_warnings()[0])
        self.assertEqual('Hello 2', lActual[0].get_suppressed_warnings()[1])
        self.assertEqual('Goodbye', lActual[1].get_suppressed_warnings()[0])

    def test_get_suppressions_which_did_not_suppress_a_warning(self):

        oSuppressionList = suppression_list.create()

        oSuppression = suppression.create('Sup0')
        oSuppression.add_suppressed_warning('Hello')
        oSuppression.add_suppressed_warning('Hello 2')
        oSuppressionList.add_suppression(oSuppression)

        oSuppression = suppression.create('Sup1')
        oSuppression.add_suppressed_warning('Goodbye')
        oSuppressionList.add_suppression(oSuppression)

        oSuppression = suppression.create('Sup2')
        oSuppressionList.add_suppression(oSuppression)

        lActual = oSuppressionList.get_suppressions_which_did_not_suppress_a_warning()

        self.assertEqual(1, len(lActual))

        self.assertEqual('Sup2', lActual[0].get_warning_id())

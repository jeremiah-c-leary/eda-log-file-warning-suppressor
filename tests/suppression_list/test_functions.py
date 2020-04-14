
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

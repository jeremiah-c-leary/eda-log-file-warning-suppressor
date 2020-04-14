
import unittest

from elfws import warning
from elfws import warning_list

class testWarningListClassMethods(unittest.TestCase):

    def test_empty_warning_list_creation(self):
        oWarningList = warning_list.create()
        self.assertEqual([], oWarningList.warnings)

    def test_add_warning_method(self):
        oWarningList = warning_list.create()

        oWarningList.add_warning(warning.create('WID1'))
        oWarningList.add_warning(warning.create('WID2'))

        self.assertEqual('WID1', oWarningList.warnings[0].warning_id)
        self.assertEqual('WID2', oWarningList.warnings[1].warning_id)

    def test_has_warnings(self):

        oWarningList = warning_list.create()

        self.assertEqual(False, oWarningList.has_warnings())

        oWarningList.add_warning(warning.create('WID1'))

        self.assertEqual(True, oWarningList.has_warnings())

    def test_get_number_of_warnings(self):

        oWarningList = warning_list.create()

        self.assertEqual(0, oWarningList.get_number_of_warnings())

        oWarningList.add_warning(warning.create('WID1'))

        self.assertEqual(1, oWarningList.get_number_of_warnings())

        oWarningList.add_warning(warning.create('WID2'))

        self.assertEqual(2, oWarningList.get_number_of_warnings())

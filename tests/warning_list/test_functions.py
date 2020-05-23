
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

    def test_get_warnings_suppressed_by_multiple_rules(self):

        oWarningList = warning_list.create()

        oWarning = warning.create('WID1')
        oWarning.add_suppression_rule('Rule 1')
        oWarning.add_suppression_rule('Rule 2')
        
        oWarningList.add_warning(oWarning)

        oWarning = warning.create('WID2')
        oWarning.add_suppression_rule('Rule 3')
        
        oWarningList.add_warning(oWarning)
        
        oWarning = warning.create('WID3')
        oWarning.add_suppression_rule('Rule 4')
        oWarning.add_suppression_rule('Rule 5')
        
        oWarningList.add_warning(oWarning)

        lActual = oWarningList.get_warnings_suppressed_by_multiple_rules()

        self.assertEqual(2, len(lActual))

        self.assertEqual('WID1', lActual[0].get_id())
        self.assertEqual('WID3', lActual[1].get_id())

    def test_maximum_id_length(self):

        oWarningList = warning_list.create()

        oWarning = warning.create('1')
        oWarningList.add_warning(oWarning)

        self.assertEqual(1,oWarningList.get_maximum_id_length())

        oWarning = warning.create('11111')
        oWarningList.add_warning(oWarning)

        self.assertEqual(5,oWarningList.get_maximum_id_length())

        oWarning = warning.create('1111111111111')
        oWarningList.add_warning(oWarning)

        self.assertEqual(13,oWarningList.get_maximum_id_length())


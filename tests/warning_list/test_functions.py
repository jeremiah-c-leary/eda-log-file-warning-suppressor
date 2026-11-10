
import unittest

from elfws import warning
from elfws import warning_list

class testWarningListClassMethods(unittest.TestCase):

    def test_empty_warning_list_creation(self):
        oWarningList = warning_list.WarningList()
        self.assertEqual([], oWarningList.warnings)

    def test_add_warning_method(self):
        oWarningList = warning_list.WarningList()

        oWarningList.add_warning(warning.LogWarning('WID1'))
        oWarningList.add_warning(warning.LogWarning('WID2'))

        self.assertEqual('WID1', oWarningList.warnings[0].warning_id)
        self.assertEqual('WID2', oWarningList.warnings[1].warning_id)

    def test_has_warnings(self):

        oWarningList = warning_list.WarningList()

        self.assertEqual(False, oWarningList.has_warnings())

        oWarningList.add_warning(warning.LogWarning('WID1'))

        self.assertEqual(True, oWarningList.has_warnings())

    def test_get_number_of_warnings(self):

        oWarningList = warning_list.WarningList()

        self.assertEqual(0, oWarningList.get_number_of_warnings())

        oWarningList.add_warning(warning.LogWarning('WID1'))

        self.assertEqual(1, oWarningList.get_number_of_warnings())

        oWarningList.add_warning(warning.LogWarning('WID2'))

        self.assertEqual(2, oWarningList.get_number_of_warnings())

    def test_get_warnings_suppressed_by_multiple_rules(self):

        oWarningList = warning_list.WarningList()

        oWarning = warning.LogWarning('WID1')
        oWarning.add_suppression_rule('Rule 1')
        oWarning.add_suppression_rule('Rule 2')
        
        oWarningList.add_warning(oWarning)

        oWarning = warning.LogWarning('WID2')
        oWarning.add_suppression_rule('Rule 3')
        
        oWarningList.add_warning(oWarning)
        
        oWarning = warning.LogWarning('WID3')
        oWarning.add_suppression_rule('Rule 4')
        oWarning.add_suppression_rule('Rule 5')
        
        oWarningList.add_warning(oWarning)

        lActual = oWarningList.get_warnings_suppressed_by_multiple_rules()

        self.assertEqual(2, len(lActual))

        self.assertEqual('WID1', lActual[0].get_id())
        self.assertEqual('WID3', lActual[1].get_id())


    def test_get_investigate_warnings(self):

        oWarningList = warning_list.WarningList()

        lExpected = []
        oWarning = warning.LogWarning('1')
        oWarning.set_investigate()
        oWarning.add_suppression_rule('Suppression_rule')
        oWarningList.add_warning(oWarning)
        lExpected.append(oWarning)

        oWarning = warning.LogWarning('2')
        oWarning.add_suppression_rule('Suppression_rule')
        oWarningList.add_warning(oWarning)

        oWarning = warning.LogWarning('3')
        oWarning.add_suppression_rule('Suppression_rule')
        oWarning.set_investigate()
        oWarningList.add_warning(oWarning)
        lExpected.append(oWarning)

        oWarning = warning.LogWarning('4')
        oWarning.add_suppression_rule('Suppression_rule')
        oWarningList.add_warning(oWarning)

        oWarning = warning.LogWarning('5')
        oWarning.add_suppression_rule('Suppression_rule')
        oWarning.set_investigate()
        oWarningList.add_warning(oWarning)
        lExpected.append(oWarning)

        oWarning = warning.LogWarning('6')
        oWarning.add_suppression_rule('Suppression_rule')
        oWarning.set_investigate()
        oWarningList.add_warning(oWarning)
        lExpected.append(oWarning)

        lActual = oWarningList.get_investigate_warnings()

        self.assertEqual(lExpected, lActual)

    def test_get_suppressed_warnings(self):

        oWarningList = warning_list.WarningList()

        lExpected = []
        oWarning = warning.LogWarning('1')
        oWarning.set_investigate()
        oWarning.add_suppression_rule('Suppression_rule')
        oWarningList.add_warning(oWarning)

        oWarning = warning.LogWarning('2')
        oWarning.add_suppression_rule('Suppression_rule')
        oWarningList.add_warning(oWarning)
        lExpected.append(oWarning)

        oWarning = warning.LogWarning('3')
        oWarning.add_suppression_rule('Suppression_rule')
        oWarning.set_investigate()
        oWarningList.add_warning(oWarning)

        oWarning = warning.LogWarning('4')
        oWarning.add_suppression_rule('Suppression_rule')
        oWarningList.add_warning(oWarning)
        lExpected.append(oWarning)

        oWarning = warning.LogWarning('5')
        oWarning.add_suppression_rule('Suppression_rule')
        oWarning.set_investigate()
        oWarningList.add_warning(oWarning)

        oWarning = warning.LogWarning('6')
        oWarning.add_suppression_rule('Suppression_rule')
        oWarning.set_investigate()
        oWarningList.add_warning(oWarning)

        lActual = oWarningList.get_suppressed_warnings()

        self.assertEqual(lExpected, lActual)



import unittest

from elfws import warning

class testWarningClassMethods(unittest.TestCase):

    def test_empty_warning_creation(self):
        oWarning = warning.create()
        self.assertEqual(None, oWarning.warning_id)
        self.assertEqual(None, oWarning.message)
        self.assertEqual(None, oWarning.filename)
        self.assertEqual(None, oWarning.linenumber)
        self.assertEqual([], oWarning.suppressed_by)
        
    def test_assignment_class_creation(self):
        oWarning = warning.create('WID', 'Message', 'Filename', 'Linenumber')
        self.assertEqual('WID', oWarning.warning_id)
        self.assertEqual('Message', oWarning.message)
        self.assertEqual('Filename', oWarning.filename)
        self.assertEqual('Linenumber', oWarning.linenumber)

    def test_get_id_method(self):
        oWarning = warning.create('WID', 'Message', 'Filename', 'Linenumber')
        self.assertEqual('WID', oWarning.get_id())

    def test_get_message_method(self):
        oWarning = warning.create('WID', 'Message', 'Filename', 'Linenumber')
        self.assertEqual('Message', oWarning.get_message())

    def test_get_filename_method(self):
        oWarning = warning.create('WID', 'Message', 'Filename', 'Linenumber')
        self.assertEqual('Filename', oWarning.get_filename())

    def test_get_linenumber_method(self):
        oWarning = warning.create('WID', 'Message', 'Filename', 'Linenumber')
        self.assertEqual('Linenumber', oWarning.get_linenumber())

    def test_is_suppressed(self):
        oWarning = warning.create()
        self.assertFalse(oWarning.is_suppressed())
        oWarning.add_suppression_rule('Rule')
        self.assertTrue(oWarning.is_suppressed())

    def test_is_suppressed_by_multiple_rules(self):
        oWarning = warning.create()
        self.assertFalse(oWarning.is_suppressed_by_multiple_rules())
        oWarning.add_suppression_rule('Rule')
        self.assertFalse(oWarning.is_suppressed_by_multiple_rules())
        oWarning.add_suppression_rule('Rule 1')
        self.assertTrue(oWarning.is_suppressed_by_multiple_rules())

    def test_add_suppression_rule(self):
        oWarning = warning.create()
        self.assertEqual([], oWarning.suppressed_by)
        oWarning.add_suppression_rule('Rule')
        self.assertEqual(['Rule'], oWarning.suppressed_by)
        oWarning.add_suppression_rule('Rule 1')
        self.assertEqual(['Rule', 'Rule 1'], oWarning.suppressed_by)

    def test_get_suppressed_by_rules(self):
        oWarning = warning.create()
        self.assertEqual([], oWarning.get_suppressed_by_rules())
        oWarning.add_suppression_rule('Rule')
        self.assertEqual(['Rule'], oWarning.get_suppressed_by_rules())
        oWarning.add_suppression_rule('Rule 1')
        self.assertEqual(['Rule', 'Rule 1'], oWarning.get_suppressed_by_rules())

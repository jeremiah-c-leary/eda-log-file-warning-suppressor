

import unittest

from elfws import warning

class testWarningClassMethods(unittest.TestCase):

    def test_empty_warning_creation(self):
        oWarning = warning.create()
        self.assertEqual(None, oWarning.warning_id)
        self.assertEqual(None, oWarning.message)
        self.assertEqual(None, oWarning.filename)
        self.assertEqual(None, oWarning.linenumber)
        
    def test_assignment_class_creation(self):
        oWarning = warning.create('WID', 'Message', 'Filename', 'Linenumber')
        self.assertEqual('WID', oWarning.warning_id)
        self.assertEqual('Message', oWarning.message)
        self.assertEqual('Filename', oWarning.filename)
        self.assertEqual('Linenumber', oWarning.linenumber)

    def test_get_warning_id_method(self):
        oWarning = warning.create('WID', 'Message', 'Filename', 'Linenumber')
        self.assertEqual('WID', oWarning.get_warning_id())

    def test_get_message_method(self):
        oWarning = warning.create('WID', 'Message', 'Filename', 'Linenumber')
        self.assertEqual('Message', oWarning.get_message())

    def test_get_filename_method(self):
        oWarning = warning.create('WID', 'Message', 'Filename', 'Linenumber')
        self.assertEqual('Filename', oWarning.get_filename())

    def test_get_linenumber_method(self):
        oWarning = warning.create('WID', 'Message', 'Filename', 'Linenumber')
        self.assertEqual('Linenumber', oWarning.get_linenumber())

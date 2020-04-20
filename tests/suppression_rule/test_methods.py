

import unittest

from elfws import suppression

class testSuppressionClassMethods(unittest.TestCase):

    def test_empty_class_creation(self):
        oSuppression = suppression.create()
        self.assertEqual(None, oSuppression.warning_id)
        self.assertEqual(None, oSuppression.message)
        self.assertEqual(None, oSuppression.author)
        self.assertEqual(None, oSuppression.comment)
        self.assertEqual([], oSuppression.suppressed_warnings)
        
    def test_assignment_class_creation(self):
        oSuppression = suppression.create('WID', 'Message', 'Author', 'comment')
        self.assertEqual('WID', oSuppression.warning_id)
        self.assertEqual('Message', oSuppression.message)
        self.assertEqual('Author', oSuppression.author)

    def test_get_warning_id_method(self):
        oSuppression = suppression.create('WID', 'Message', 'Author', 'comment')
        self.assertEqual('WID', oSuppression.get_warning_id())

    def test_get_message_method(self):
        oSuppression = suppression.create('WID', 'Message', 'Author', 'comment')
        self.assertEqual('Message', oSuppression.get_message())

    def test_get_author_method(self):
        oSuppression = suppression.create('WID', 'Message', 'Author', 'comment')
        self.assertEqual('Author', oSuppression.get_author())

    def test_get_comment_method(self):
        oSuppression = suppression.create('WID', 'Message', 'Author', 'comment')
        self.assertEqual('comment', oSuppression.get_comment())

    def test_add_suppressed_warning(self):
        oSuppression = suppression.create()
        self.assertEqual(0, len(oSuppression.suppressed_warnings))
        oSuppression.add_suppressed_warning('Hello')
        self.assertEqual(1, len(oSuppression.suppressed_warnings))
        oSuppression.add_suppressed_warning('Goodbye')
        self.assertEqual(2, len(oSuppression.suppressed_warnings))
        self.assertEqual('Hello', oSuppression.suppressed_warnings[0])
        self.assertEqual('Goodbye', oSuppression.suppressed_warnings[1])

    def test_get_suppressed_warnings(self):
        oSuppression = suppression.create()
        self.assertEqual([], oSuppression.get_suppressed_warnings())
        oSuppression.add_suppressed_warning('Hello')
        self.assertEqual(['Hello'], oSuppression.get_suppressed_warnings())
        oSuppression.add_suppressed_warning('Goodbye')
        self.assertEqual(['Hello', 'Goodbye'], oSuppression.get_suppressed_warnings())

    def test_has_suppressed_a_warning(self):
        oSuppression = suppression.create()
        self.assertFalse(oSuppression.has_suppressed_a_warning())
        oSuppression.add_suppressed_warning('Hello')
        self.assertTrue(oSuppression.has_suppressed_a_warning())



import unittest

from lws import suppression

class testSuppressionClassMethods(unittest.TestCase):

    def test_empty_class_creation(self):
        oSuppression = suppression.create()
        self.assertEqual(None, oSuppression.warning_id)
        self.assertEqual(None, oSuppression.message)
        self.assertEqual(None, oSuppression.author)
        self.assertEqual(None, oSuppression.comment)
        
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

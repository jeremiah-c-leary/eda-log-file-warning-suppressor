
import unittest

from elfws import suppression
from elfws import utils
from elfws import warning


class test_functions(unittest.TestCase):

    def test_basic_matching_passing(self):
       oWarning = warning.create('first_id')
       oSuppression = suppression.create('first_id')
       self.assertTrue(utils.do_ids_match(oWarning, oSuppression))

    def test_basic_matching_failing(self):
       oWarning = warning.create('First_id')
       oSuppression = suppression.create('first_id')
       self.assertFalse(utils.do_ids_match(oWarning, oSuppression))

    def test_regexp_ending(self):
       oWarning = warning.create('first_.*')
       oSuppression = suppression.create('first_id')
       self.assertTrue(utils.do_ids_match(oWarning, oSuppression))

    def test_regexp_single_character(self):
       oWarning = warning.create('fi.st')
       oSuppression = suppression.create('first_id')
       self.assertTrue(utils.do_ids_match(oWarning, oSuppression))

    def test_regexp_beginning(self):
       oWarning = warning.create('.*_id')
       oSuppression = suppression.create('first_id')
       self.assertTrue(utils.do_ids_match(oWarning, oSuppression))


       

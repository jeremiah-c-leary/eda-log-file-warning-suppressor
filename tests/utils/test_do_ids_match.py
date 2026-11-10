
import unittest

from elfws import suppression
from elfws import utils
from elfws import warning


class test_functions(unittest.TestCase):

    def test_basic_matching_passing(self):
       oWarning = warning.LogWarning('first_id')
       oSuppression = suppression.Suppression('first_id')
       self.assertTrue(utils.do_ids_match(oWarning, oSuppression))

    def test_basic_matching_failing(self):
       oWarning = warning.LogWarning('First_id')
       oSuppression = suppression.Suppression('first_id')
       self.assertFalse(utils.do_ids_match(oWarning, oSuppression))

    def test_regexp_ending(self):
       oWarning = warning.LogWarning('first_id')
       oSuppression = suppression.Suppression('first_.*')
       self.assertTrue(utils.do_ids_match(oWarning, oSuppression))

    def test_regexp_single_character(self):
       oWarning = warning.LogWarning('first_id')
       oSuppression = suppression.Suppression('fi.st_id')
       self.assertTrue(utils.do_ids_match(oWarning, oSuppression))

    def test_regexp_beginning(self):
       oWarning = warning.LogWarning('first_id')
       oSuppression = suppression.Suppression('.*_id')
       self.assertTrue(utils.do_ids_match(oWarning, oSuppression))

    def test_regexp_dot_star(self):
       oWarning = warning.LogWarning('first_id')
       oSuppression = suppression.Suppression('.*')
       self.assertTrue(utils.do_ids_match(oWarning, oSuppression))



       

    def test_id_does_not_match_as_prefix(self):
       oWarning = warning.LogWarning('Synth 8-10')
       oSuppression = suppression.Suppression('Synth 8-1')
       self.assertFalse(utils.do_ids_match(oWarning, oSuppression))

    def test_id_with_trailing_characters_does_not_match(self):
       oWarning = warning.LogWarning('first_id_extra')
       oSuppression = suppression.Suppression('first_id')
       self.assertFalse(utils.do_ids_match(oWarning, oSuppression))

    def test_explicit_prefix_regexp_matches(self):
       oWarning = warning.LogWarning('Synth 8-10')
       oSuppression = suppression.Suppression('Synth 8-1.*')
       self.assertTrue(utils.do_ids_match(oWarning, oSuppression))

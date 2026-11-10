
import unittest

from elfws import suppression
from elfws import rule_matching
from elfws import warning


class test_functions(unittest.TestCase):

    def test_id_and_message_match(self):
        oWarning = warning.LogWarning('Synth 8-1', 'Port I_CLK is not used')
        oSuppression = suppression.Suppression('Synth 8-1', 'I_CLK')
        self.assertTrue(rule_matching.check_for_match(oWarning, oSuppression))

    def test_id_matches_but_message_does_not(self):
        oWarning = warning.LogWarning('Synth 8-1', 'Port I_CLK is not used')
        oSuppression = suppression.Suppression('Synth 8-1', 'I_RST')
        self.assertFalse(rule_matching.check_for_match(oWarning, oSuppression))

    def test_message_matches_but_id_does_not(self):
        oWarning = warning.LogWarning('Synth 8-1', 'Port I_CLK is not used')
        oSuppression = suppression.Suppression('Synth 8-2', 'I_CLK')
        self.assertFalse(rule_matching.check_for_match(oWarning, oSuppression))

    def test_neither_matches(self):
        oWarning = warning.LogWarning('Synth 8-1', 'Port I_CLK is not used')
        oSuppression = suppression.Suppression('Synth 8-2', 'I_RST')
        self.assertFalse(rule_matching.check_for_match(oWarning, oSuppression))

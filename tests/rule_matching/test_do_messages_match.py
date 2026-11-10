
import unittest

from elfws import suppression
from elfws import rule_matching
from elfws import warning


class test_functions(unittest.TestCase):

    def test_exact_message_matches(self):
        oWarning = warning.LogWarning('ID', 'Port I_CLK is not used')
        oSuppression = suppression.Suppression('ID', 'Port I_CLK is not used')
        self.assertTrue(rule_matching.do_messages_match(oWarning, oSuppression))

    def test_message_matches_anywhere_in_warning(self):
        oWarning = warning.LogWarning('ID', 'Port I_CLK is not used')
        oSuppression = suppression.Suppression('ID', 'I_CLK')
        self.assertTrue(rule_matching.do_messages_match(oWarning, oSuppression))

    def test_message_regular_expression(self):
        oWarning = warning.LogWarning('ID', 'Port I_DATA[3] is not used')
        oSuppression = suppression.Suppression('ID', r'I_DATA\[[0-9]+\]')
        self.assertTrue(rule_matching.do_messages_match(oWarning, oSuppression))

    def test_message_does_not_match(self):
        oWarning = warning.LogWarning('ID', 'Port I_CLK is not used')
        oSuppression = suppression.Suppression('ID', 'I_RST')
        self.assertFalse(rule_matching.do_messages_match(oWarning, oSuppression))

    def test_message_is_case_sensitive(self):
        oWarning = warning.LogWarning('ID', 'Port I_CLK is not used')
        oSuppression = suppression.Suppression('ID', 'port i_clk')
        self.assertFalse(rule_matching.do_messages_match(oWarning, oSuppression))

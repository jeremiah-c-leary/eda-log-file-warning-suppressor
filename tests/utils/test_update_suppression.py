
import unittest

from elfws import suppression
from elfws import utils


def build_rule(dSup):
    oSupRule = suppression.Suppression('ID', 'msg')
    utils.update_suppression_author(oSupRule, dSup)
    utils.update_suppression_comment(oSupRule, dSup)
    utils.update_suppression_investigate(oSupRule, dSup)
    utils.update_suppression_options(oSupRule, dSup)
    return oSupRule


class test_update_suppression(unittest.TestCase):

    def test_missing_keys_use_defaults(self):
        oSupRule = build_rule({'msg': 'msg'})
        self.assertEqual('<None>', oSupRule.get_author())
        self.assertEqual('<None>', oSupRule.get_comment())
        self.assertFalse(oSupRule.get_investigate())
        self.assertEqual([], oSupRule.options)

    def test_present_keys_are_used(self):
        oSupRule = build_rule({'msg': 'msg', 'author': 'jcl', 'comment': 'why', 'investigate': True, 'options': ['opt']})
        self.assertEqual('jcl', oSupRule.get_author())
        self.assertEqual('why', oSupRule.get_comment())
        self.assertTrue(oSupRule.get_investigate())
        self.assertEqual(['opt'], oSupRule.options)

    def test_keys_present_with_empty_values(self):
        oSupRule = build_rule({'msg': 'msg', 'author': None, 'comment': None, 'investigate': None, 'options': None})
        self.assertEqual(None, oSupRule.get_author())
        self.assertEqual(None, oSupRule.get_comment())
        self.assertFalse(oSupRule.get_investigate())
        self.assertEqual([], oSupRule.options)

    def test_investigate_false_and_empty_options(self):
        oSupRule = build_rule({'msg': 'msg', 'investigate': False, 'options': []})
        self.assertFalse(oSupRule.get_investigate())
        self.assertEqual([], oSupRule.options)

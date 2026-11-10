
import unittest

from elfws import suppression_file
from elfws import error


def build(dRules):
    return {'suppress': {'rules': dRules}}


class test_rule_validation(unittest.TestCase):

    def assert_raises_errors(self, dSuppression, lExpectedErrors):
        with self.assertRaises(error.ElfwsError) as oContext:
            suppression_file.create_suppression_list(dSuppression)
        self.assertEqual(1, oContext.exception.iExitCode)
        sMessage = str(oContext.exception)
        for sError in lExpectedErrors:
            self.assertIn(sError, sMessage)
        return sMessage

    def test_valid_rules_are_all_loaded(self):
        dSup = build({'A': [{'msg': 'x'}, {'msg': 'y'}], 'B': [{'msg': 'z'}]})
        self.assertEqual(3, suppression_file.create_suppression_list(dSup).get_number_of_suppressions())

    def test_missing_msg_reports_error_and_does_not_hide_other_errors(self):
        dSup = build({'A': [{'msg': 'x'}, {'comment': 'no msg'}, {'msg': 'y['}], 'B': [{'author': 'me'}]})
        self.assert_raises_errors(dSup, [
            'suppress -> rules -> A[1]: rule is missing the required "msg" key',
            'suppress -> rules -> A[2]: invalid regular expression in msg',
            'suppress -> rules -> B[0]: rule is missing the required "msg" key',
        ])

    def test_empty_msg_value_is_an_error(self):
        self.assert_raises_errors(build({'A': [{'msg': None}]}), ['A[0]: rule is missing the required "msg" key'])

    def test_invalid_id_regular_expression(self):
        self.assert_raises_errors(build({'Synth[': [{'msg': 'x'}]}), ["invalid regular expression in warning id 'Synth['"])

    def test_invalid_msg_regular_expression(self):
        self.assert_raises_errors(build({'A': [{'msg': 'port[3'}]}), ["invalid regular expression in msg 'port[3'"])

    def test_rules_for_id_not_a_list(self):
        self.assert_raises_errors(build({'A': {'msg': 'x'}}), ['suppress -> rules -> A: expected a list of rules'])

    def test_rule_not_a_mapping(self):
        self.assert_raises_errors(build({'A': ['just a string']}), ['A[0]: expected a rule with a "msg" key'])

    def test_rules_not_a_mapping(self):
        self.assert_raises_errors(build(['A']), ['suppress -> rules: expected warning ids'])

    def test_group_not_a_mapping(self):
        dSup = {'suppress': {'group_1': 'not a group'}}
        self.assert_raises_errors(dSup, ['suppress -> group_1: expected a group or "rules" key'])

    def test_error_path_includes_groups(self):
        dSup = {'suppress': {'group_1': {'group_2': {'rules': {'A': [{'comment': 'x'}]}}}}}
        self.assert_raises_errors(dSup, ['suppress -> group_1 -> group_2 -> rules -> A[0]'])

    def test_top_level_not_a_mapping(self):
        self.assert_raises_errors(['suppress'], ['must contain a mapping'])

    def test_empty_suppress_and_rules_sections_are_allowed(self):
        self.assertEqual(0, suppression_file.create_suppression_list({'suppress': None}).get_number_of_suppressions())
        self.assertEqual(0, suppression_file.create_suppression_list(build(None)).get_number_of_suppressions())
        self.assertEqual(0, suppression_file.create_suppression_list({}).get_number_of_suppressions())

    def test_numeric_ids_and_messages_are_converted_to_strings(self):
        oSupList = suppression_file.create_suppression_list(build({1234: [{'msg': 56}]}))
        oSup = oSupList.get_suppressions()[0]
        self.assertEqual('1234', oSup.get_warning_id())
        self.assertEqual('56', oSup.get_message())

    def test_python_specific_yaml_tags_are_rejected(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as sDir:
            sFile = os.path.join(sDir, 'suppress.yaml')
            with open(sFile, 'w') as oFile:
                oFile.write('suppress: !!python/tuple [1, 2]\n')
            with self.assertRaises(error.ElfwsError) as oContext:
                suppression_file.read_suppression_file(sFile)
        self.assertEqual(1, oContext.exception.iExitCode)

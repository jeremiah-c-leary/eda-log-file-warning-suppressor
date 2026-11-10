
import unittest

from elfws.vendor import utils


class test_vendor_utils(unittest.TestCase):

    def test_sequence_at_start_of_file(self):
        lFile = ['Header', '----', 'data']
        self.assertTrue(utils.sequence_of_lines_starts_with(1, lFile, ['Header', '----']))

    def test_sequence_later_in_file(self):
        lFile = ['x', 'Header', '----', 'data']
        self.assertTrue(utils.sequence_of_lines_starts_with(2, lFile, ['Header', '----']))
        self.assertFalse(utils.sequence_of_lines_starts_with(1, lFile, ['Header', '----']))

    def test_sequence_longer_than_preceding_lines(self):
        lFile = ['----', 'data']
        self.assertFalse(utils.sequence_of_lines_starts_with(0, lFile, ['Header', '----']))

    def test_split_id_and_message(self):
        self.assertEqual(('ABC', 'msg here'), utils.split_id_and_message('Warning: ABC: msg here'))
        self.assertEqual(('ABC', 'msg: with colon'), utils.split_id_and_message('Warning: ABC: msg: with colon'))
        self.assertEqual(('ABC', ''), utils.split_id_and_message('Warning: ABC:'))

    def test_split_id_and_message_without_id_separator(self):
        self.assertEqual((utils.NO_ID, 'no id in this message'), utils.split_id_and_message('Warning: no id in this message'))

    def test_reject_ids_containing_spaces(self):
        sLine = 'Warning: has spaces: msg'
        self.assertEqual((utils.NO_ID, 'has spaces: msg'), utils.reject_ids_containing_spaces(sLine, 'has spaces', 'msg'))
        self.assertEqual(('ABC', 'msg'), utils.reject_ids_containing_spaces('Warning: ABC: msg', 'ABC', 'msg'))


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

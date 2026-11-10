
import unittest

from elfws import log_file


class test_functions(unittest.TestCase):

    def test_read_log_file(self):
        lExpected = []
        lExpected.append('Microsemi Libero Software')
        lExpected.append('Version: 11.9.2.1')
        lExpected.append('Release: 11.9 SP2')
        lExpected.append('')
        lExpected.append('Created a new design.')
        lExpected.append('')
        lExpected.append('# This is a warning with an ID')
        lExpected.append('Warning: DEF1234 : This is a warning')
        lExpected.append('')
        lExpected.append('# This is a warning without an ID')
        lExpected.append('Warning: This is a warning without an ID')
        lExpected.append('Warning: This is a warning with a : that does not have an ID')
        lExpected.append('')
        lExpected.append('# This is a multiline warning with an ID')
        lExpected.append('Warning: MULTI546 : This is the first line of the warning')
        lExpected.append('         This is the second line of the warning')
        lExpected.append(' This is the last line of the warning.')
        lExpected.append('')
        lExpected.append('# This is a multiline warning without an ID')
        lExpected.append('Warning: This is the first line : of the message')
        lExpected.append(' This is the second line of the message')
        lExpected.append('   This is the third line of the message')
        lExpected.append('  This is the last line of the message.')
        lExpected.append('')
        lExpected.append('#These should not be counted as warnings:')
        lExpected.append(' Warning: ABC5425 : this is not a warning because of the leading space')
        lExpected.append('')
        lExpected.append('')

        self.assertEqual(lExpected, log_file.read_log_file('tests/vendor/microsemi/designer/warning_messages.log'))

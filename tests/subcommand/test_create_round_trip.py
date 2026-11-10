
import unittest

from elfws import parser_loader
from elfws import rule_matching
from elfws import suppression_file
from elfws.subcommand import create


lLogFile = [
    'Microsemi Libero Software',
    'Warning: ID1: Port I_DATA[3:0] is not used',
    'Warning: ID2: Net (a+b)*c? is unconnected {x|y}',
    'Warning: ID3: Path C:\\temp\\file.v ^ $HOME.',
    'Info',
]


class test_create_round_trip(unittest.TestCase):

    def test_escape_regular_expression(self):
        self.assertEqual('Port I_DATA\\[3:0\\] \\(x\\) a\\.b', create.escape_regular_expression('Port I_DATA[3:0] (x) a.b'))

    def test_created_rules_suppress_the_warnings_they_were_created_from(self):
        oWarnList = parser_loader.create_warning_list(lLogFile, 'logfile')
        self.assertEqual(3, oWarnList.get_number_of_warnings())

        dSup = create.create_suppression_dict(oWarnList)
        oSupList = suppression_file.create_suppression_list(dSup)
        rule_matching.apply_suppression_rules_to_warnings(oWarnList, oSupList)

        self.assertEqual([], oWarnList.get_unsuppressed_warnings())
        self.assertEqual([], oWarnList.get_warnings_suppressed_by_multiple_rules())

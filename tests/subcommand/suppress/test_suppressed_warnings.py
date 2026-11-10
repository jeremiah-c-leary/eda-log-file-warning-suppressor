
import unittest

from elfws.subcommand import create


def file_path(sFilename):
    return 'tests/subcommand/suppress/' + sFilename


class test_suppressed_warnings(unittest.TestCase):

    def test_create_only_includes_warnings_not_already_suppressed(self):
        lActual = create.extract_warnings_to_suppress('tests/vendor/microsemi/designer/warning_messages.log', file_path('suppress_microsemi_designer_logfile.yaml'))

        self.assertEqual(1, len(lActual))

        self.assertEqual('MULTI546', lActual[0].get_id())
        self.assertEqual('This is the first line of the warning This is the second line of the warning This is the last line of the warning.', lActual[0].get_message())

    def test_create_includes_every_warning_without_a_suppression_file(self):
        lActual = create.extract_warnings_to_suppress('tests/vendor/microsemi/designer/warning_messages.log', None)

        self.assertEqual(5, len(lActual))

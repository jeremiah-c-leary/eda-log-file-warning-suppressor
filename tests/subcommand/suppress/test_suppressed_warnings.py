
import os
import unittest


from elfws.subcommand import suppress
from elfws import utils
from elfws import warning

from elfws.vendor.microsemi import designer


def file_path(sFilename):
    return 'tests/subcommand/suppress/' + sFilename


class test_suppressed_warnings(unittest.TestCase):

    def test_extract_non_suppressed_warnings(self):
        dSup = utils.read_suppression_file(file_path('suppress_microsemi_designer_logfile.yaml'))
        oSupList = utils.create_suppression_list(dSup)

        lLogFile = utils.read_log_file('tests/vendor/microsemi/designer/warning_messages.log')
        oWarnList = designer.extract_warnings(lLogFile)

        oActual = suppress.extract_non_suppressed_warnings(oWarnList, oSupList)

        self.assertEqual(1, oActual.get_number_of_warnings())

        self.assertEqual('MULTI546', oActual.warnings[0].get_id())
        self.assertEqual('This is the first line of the warning This is the second line of the warning This is the last line of the warning.', oActual.warnings[0].get_message())


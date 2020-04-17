

import unittest
from unittest import mock

from elfws import version as version_number
from elfws.subcommand import version

class testVersionModule(unittest.TestCase):

    @mock.patch('sys.stdout')
    def test_version(self, mockStdout):
        try:
            version.print_version()
        except SystemExit:
            pass

        mockStdout.write.assert_has_calls([
            mock.call('EDA Log File Warning Suppressor (ELFWS) version ' + version_number.version),
            mock.call('\n')
        ])

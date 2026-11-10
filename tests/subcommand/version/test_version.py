

import unittest
from unittest import mock

from elfws import version as version_number
from elfws.subcommand import version

class testVersionModule(unittest.TestCase):

    @mock.patch('sys.stdout')
    def test_version(self, mockStdout):
        with self.assertRaises(SystemExit) as oContext:
            version.print_version()

        self.assertEqual(oContext.exception.code, 0)

        mockStdout.write.assert_has_calls([
            mock.call('EDA Log File Warning Suppressor (ELFWS) version ' + version_number.version),
            mock.call('\n')
        ])

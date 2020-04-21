
import unittest
from unittest import mock
import sys

from datetime import datetime

from elfws import __main__
from elfws import version
from elfws import utils


class test_arguments(unittest.TestCase):

#    def setUp(self):
#        datetime_patcher = mock.patch.object(
#            tests.elfws.test_main.test_arguments.datetime, 'datetime',
#            mock.Mock(wraps=datetime.datetime)
#        )
#        mocked_datetime = datetime_patcher.start()
#        mocked_datetime.today.return_value = datetime.datetime(2012, 6, 16)
#        self.addCleanup(datetime_patcher.stop)

    @mock.patch('sys.stdout')
    def test_version(self, mockStdout):
        sys.argv = ['elfws', 'version']
        try:
            __main__.main()
        except SystemExit:
            pass

        mockStdout.write.assert_has_calls([
            mock.call('EDA Log File Warning Suppressor (ELFWS) version ' + version.version), mock.call('\n')
        ])

    @mock.patch('sys.stdout')
    @mock.patch('elfws.display.datetime')
    def test_show(self, mock_datetime, mock_stdout):
        mock_datetime.now.return_value = 'Some Date'
        sys.argv = ['elfws', 'show', 'tests/vendor/microsemi/designer/warning_messages.log']
        __main__.main()

        lLogFile = utils.read_log_file('tests/elfws/show_output.txt')
        
        lExpected = []
        for sLine in lLogFile:
            lExpected.append(mock.call(sLine))
            lExpected.append(mock.call('\n'))

        mock_stdout.write.assert_has_calls(lExpected)


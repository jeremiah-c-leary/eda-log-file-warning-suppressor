
import datetime
import unittest
from unittest import mock

from elfws import junit


class test_junit_format(unittest.TestCase):

    @mock.patch('elfws.junit.datetime')
    def test_timestamp_uses_24_hour_clock(self, mock_datetime):
        mock_datetime.datetime.now.return_value = datetime.datetime(2026, 11, 9, 14, 5, 6)
        oTestsuite = junit.TestSuite('suite', '0')
        self.assertEqual('2026-11-09T14:05:06', oTestsuite.timestamp)

    @mock.patch('elfws.junit.platform.uname', return_value=('Linux', 'host<&>"', '', '', '', ''))
    def test_attributes_are_escaped(self, mock_uname):
        oTestsuite = junit.TestSuite('suite "a" & <b>', '0')
        oTestcase = junit.TestCase('case "c"', '0', 'class <d>')
        oFailure = junit.Failure('type \'e\'')
        oFailure.add_text('text')
        oTestcase.add_failure(oFailure)
        oTestsuite.add_testcase(oTestcase)
        sXml = '\n'.join(oTestsuite.build_junit())
        self.assertIn('name="suite &quot;a&quot; &amp; &lt;b&gt;"', sXml)
        self.assertIn('hostname="host&lt;&amp;&gt;&quot;"', sXml)
        self.assertIn('<testcase name="case &quot;c&quot;" time="0" classname="class &lt;d&gt;">', sXml)
        self.assertIn('<failure type="type &apos;e&apos;">', sXml)

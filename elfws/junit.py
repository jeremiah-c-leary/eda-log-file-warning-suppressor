import platform
import datetime


class Failure():
    '''
    This class holds failure type attributes.
    '''

    def __init__(self, sType):
        self.type = sType
        self.text = []

    def add_text(self, sText):
        self.text.append(sText)

    def build_junit(self):
        '''
        Return a formatted failure as a list of strings.
        '''
        lJunit = ['    <failure type="' + escape_xml_characters(self.type) + '">']
        for sText in self.text:
            lJunit.append('      ' + escape_xml_characters(sText))
        lJunit.append('    </failure>')

        return lJunit


class TestCase():
    '''
    This class holds testcase attributes.
    '''

    def __init__(self, sName=None, sTime=None, sClassName=None):
        self.name = sName
        self.time = sTime
        self.classname = sClassName
        self.failures = []

    def add_failure(self, oFailure):
        self.failures.append(oFailure)

    def build_junit(self):
        '''
        Return formatted testcase as a list of strings.
        '''

        lJunit = ['  <testcase name="' + escape_xml_characters(self.name) + '" time="' + escape_xml_characters(self.time) + '" classname="' + escape_xml_characters(self.classname) + '">']

        for oFailure in self.failures:
            lJunit.extend(oFailure.build_junit())

        lJunit.append('  </testcase>')

        return lJunit


class TestSuite():
    '''
    This class holds testsuite attributes.
    '''

    def __init__(self, sName, sTime):
        self.name = sName
        self.time = sTime
        self.testcases = []
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    def add_testcase(self, oTestcase):
        self.testcases.append(oTestcase)

    def build_junit(self):
        '''
        Return a formatted testsuite as a list of strings.
        '''
        sHeader = '<testsuite'
        sHeader += ' errors="0"'
        sHeader += ' hostname="' + escape_xml_characters(platform.uname()[1]) + '"'
        iFailures = 0
        for oTestcase in self.testcases:
            iFailures += len(oTestcase.failures)
        sHeader += ' failures="' + str(iFailures) + '"'
        sHeader += ' timestamp="' + self.timestamp + '"'
        sHeader += ' tests="' + str(len(self.testcases)) + '"'
        sHeader += ' time="' + escape_xml_characters(self.time) + '"'
        sHeader += ' name="' + escape_xml_characters(self.name) + '"'
        sHeader += '>'
        lJunit = [sHeader]
        lJunit.append('  <properties>')
        lJunit.append('  </properties>')
        for oTestcase in self.testcases:
            lJunit.extend(oTestcase.build_junit())
        lJunit.append('  <system-out>')
        lJunit.append('  </system-out>')
        lJunit.append('  <system-err>')
        lJunit.append('  </system-err>')
        lJunit.append('</testsuite>')

        return lJunit


class XmlFile():
    '''
    This class holds testsuites.
    '''

    def __init__(self):
        self.testsuites = []

    def add_testsuite(self, oTestsuite):
        self.testsuites.append(oTestsuite)

    def build_junit(self):
        '''
        Return a JUnit XML file formatted as a list of strings.
        '''
        lJunit = ['<?xml version="1.0" ?>']
        for oTestsuite in self.testsuites:
            lJunit.extend(oTestsuite.build_junit())

        return lJunit


def escape_xml_characters(sString):
    '''
    Replaces the following characters in a string:

      &  with &amp;
      "  with &quot;
      '  with &apos;
      <  with &lt;
      >  with &gt;

    Parameters:

        sString : (string)

    Returns: (string)
    '''
    sReturn = sString.replace('&', '&amp;')
    sReturn = sReturn.replace('"', '&quot;')
    sReturn = sReturn.replace('\'', '&apos;')
    sReturn = sReturn.replace('<', '&lt;')
    sReturn = sReturn.replace('>', '&gt;')
    return sReturn

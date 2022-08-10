
import re
import sys

from elfws import display
from elfws.report import junit
from elfws import suppression_list
from elfws import utils


def show(cla):

    oSupList = suppression_list.create()

    lLogFile = utils.read_log_file(cla.log_file)

    oWarnList = utils.create_warning_list(lLogFile, cla.log_file)

    display.results(cla.log_file, '<None>', oSupList, oWarnList)

    if cla.junit:
        lJUnitFile = junit.generate_junit_xml_file(cla, oWarnList, oSupList)
        utils.write_file(cla.junit, lJUnitFile)

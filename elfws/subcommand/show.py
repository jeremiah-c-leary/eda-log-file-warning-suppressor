
import re
import sys

from elfws import utils
from elfws import display
from elfws import suppression_list


def show(cla):

    oSupList = suppression_list.create()

    lLogFile = utils.read_log_file(cla.log_file)

    oWarnList = utils.create_warning_list(lLogFile, cla.log_file)

    display.results(cla.log_file, '<None>', oSupList, oWarnList)

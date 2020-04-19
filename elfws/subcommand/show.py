
import re
import sys

from elfws import utils
from elfws import display


def show(cla):

    lLogFile = utils.read_log_file(cla.log_file)

    oWarnList = utils.create_warning_list(lLogFile, cla.log_file)

    display.results(cla.log_file, '<None>', oWarnList.get_number_of_warnings(), oWarnList)

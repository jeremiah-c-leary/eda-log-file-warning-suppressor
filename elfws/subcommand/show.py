
import re
import sys

from elfws import warning_list
from elfws import utils


def show(cla):

    lLogFile = utils.read_log_file(cla.log_file)

    try:
        mTool = utils.get_vendor_tool_module(lLogFile)
        oWarnList = mTool.extract_warnings(lLogFile)
    except AttributeError:
        print('ERROR: Log file ' + cla.log_file + ' is not supported.')
        sys.exit(1)

    for oWarning in oWarnList.get_warnings():
#        print(oWarning.get_id() + '  [' + str(oWarning.get_linenumber()) + '] ' + oWarning.get_message())
        print("| {0:<20s} | {1:>5d} | {2:s}".format(oWarning.get_id(), oWarning.get_linenumber(), oWarning.get_message()))


import sys

from elfws import parser_loader
from elfws.exit_code import ExitCode


def read_warning_list(sFileName):
    lLogFile = read_log_file(sFileName)
    return parser_loader.create_warning_list(lLogFile, sFileName)


def read_log_file(sFileName):
    '''
    Reads a log file and strips off line endings.

    Parameters:

      sFileName : (string)

    Bytes which are not valid UTF-8 are replaced rather than causing an
    error, as EDA tools frequently write other encodings.

    Exits with code 6 if the file cannot be read.

    Returns: (list of strings)
    '''
    try:
        return read_lines_without_line_endings(sFileName)
    except OSError as e:
        exit_with_log_file_error(sFileName, e)


def read_lines_without_line_endings(sFileName):
    lLines = []
    with open(sFileName, encoding='utf-8', errors='replace') as oFile:
        for sLine in oFile:
            lLines.append(sLine.rstrip())
    return lLines


def exit_with_log_file_error(sFileName, oError):
    print('ERROR: Could not read log file ' + sFileName + ' : ' + str(oError))
    sys.exit(ExitCode.LOG_FILE_READ_ERROR)


import sys

from elfws.exit_code import ExitCode


def write_junit_file(sFilename, lFile):
    write_file(sFilename, lFile, ExitCode.JUNIT_FILE_WRITE_ERROR)


def write_report_file(sFilename, lFile):
    write_file(sFilename, lFile, ExitCode.REPORT_FILE_WRITE_ERROR)


def write_file(sFilename, lFile, iExitCode):
    '''
    Writes a list of strings to a file.

    Parameters:

      sFilename : (string)

      lFile : (list of strings)

    Returns: nothing
    '''
    try:
        with open(sFilename, 'w') as oFile:
            for sLine in lFile:
                oFile.write(sLine + '\n')
    except PermissionError as err:
        print(err, "Could not write to file " + sFilename)
        sys.exit(iExitCode)

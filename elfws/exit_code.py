
import enum


class ExitCode(enum.IntEnum):
    '''
    Exit codes reported by ELFWS.

    These values are part of the command line interface and are documented
    in docs/source/exit_codes.rst.  Do not renumber them.
    '''
    SUCCESS = 0
    SUPPRESSION_FILE_ERROR = 1
    NO_MATCHING_PARSER = 2
    NO_COMMAND_LINE_ARGUMENTS = 3
    REPORT_FILE_WRITE_ERROR = 4
    JUNIT_FILE_WRITE_ERROR = 5
    LOG_FILE_READ_ERROR = 6


def do_lines_start_with_sequence(iLastLineNumber, lFile, lSequence):
    if would_sequence_start_before_first_line(iLastLineNumber, lSequence):
        return False
    iFirstLineNumber = iLastLineNumber - (len(lSequence) - 1)
    for iOffset, sExpectedStart in enumerate(lSequence):
        if not lFile[iFirstLineNumber + iOffset].startswith(sExpectedStart):
            return False
    return True


def would_sequence_start_before_first_line(iLastLineNumber, lSequence):
    return iLastLineNumber < len(lSequence) - 1


NO_ID = 'NO_ID'

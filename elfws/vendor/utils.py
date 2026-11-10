
def sequence_of_lines_starts_with(iLastLineNumber, lFile, lSequence):
    if sequence_would_start_before_first_line(iLastLineNumber, lSequence):
        return False
    iFirstLineNumber = iLastLineNumber - (len(lSequence) - 1)
    for iOffset, sExpectedStart in enumerate(lSequence):
        if not lFile[iFirstLineNumber + iOffset].startswith(sExpectedStart):
            return False
    return True


def sequence_would_start_before_first_line(iLastLineNumber, lSequence):
    return iLastLineNumber < len(lSequence) - 1

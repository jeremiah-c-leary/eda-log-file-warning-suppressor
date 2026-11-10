
def sequence_of_lines_starts_with(iLineNumber, lFile, lSequence):
    if sequence_would_start_before_first_line(iLineNumber, lSequence):
        return False
    iTemp = len(lSequence) - 1
    for x in range(len(lSequence)):
        if not lFile[iLineNumber - iTemp + x].startswith(lSequence[x]):
            return False
    return True


def sequence_would_start_before_first_line(iLineNumber, lSequence):
    return iLineNumber < len(lSequence) - 1

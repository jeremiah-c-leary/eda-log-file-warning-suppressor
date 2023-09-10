
def sequence_of_lines_starts_with(iLineNumber, lFile, lSequence):
    if iLineNumber < len(lSequence):
        return False
    iTemp = len(lSequence) - 1
    for x in range(len(lSequence)):
        if not lFile[iLineNumber - iTemp + x].startswith(lSequence[x]):
            return False
    return True


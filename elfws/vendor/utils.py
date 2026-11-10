
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


NO_ID = 'NO_ID'


def split_id_and_message(sLine):
    '''
    Splits a line formatted as "<keyword>: <id>: <message>".

    Lines without a separator between the id and message return NO_ID
    and the text after the keyword.

    Parameters:

      sLine : (string)

    Returns: (tuple of strings) id, message
    '''
    sText = text_after_keyword(sLine)
    if not has_id_separator(sText):
        return NO_ID, sText.strip()
    sId, sMessage = sText.split(':', 1)
    return sId.strip(), sMessage.strip()


def reject_ids_containing_spaces(sLine, sId, sMessage):
    '''
    Treats an id containing spaces as part of the message.

    Parameters:

      sLine : (string)

      sId : (string)

      sMessage : (string)

    Returns: (tuple of strings) id, message
    '''
    if not contains_spaces(sId):
        return sId, sMessage
    return NO_ID, text_after_keyword(sLine).strip()


def text_after_keyword(sLine):
    return sLine.split(':', 1)[1]


def has_id_separator(sText):
    return ':' in sText


def contains_spaces(sText):
    return ' ' in sText

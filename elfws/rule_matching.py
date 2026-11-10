
import re


def apply_suppression_rules_to_warnings(oWarnList, oSupList):
    for oWarning in oWarnList.get_warnings():
        for oSuppression in oSupList.get_suppressions():
            suppress_warning_with_rule(oWarning, oSuppression)


def suppress_warning_with_rule(oWarning, oSuppression):
    '''
    Suppresses a warning based on a suppression rule.

    Parameters:

        oWarning : (warning object)

        oSuppression : (suppression rule object)

    Returns: Nothing
    '''
    if check_for_match(oWarning, oSuppression):
        oSuppression.add_suppressed_warning(oWarning)
        oWarning.add_suppression_rule(oSuppression)
        if oSuppression.get_investigate():
            oWarning.set_investigate()


def check_for_match(oWarning, oSuppression):
    '''
    Compares the IDs and messages between a warning and a suppression rule.

    Parameters:

        oWarning : (warning object)

        oSuppression : (suppression rule object)

    Returns: Boolean
    '''
    return do_ids_match(oWarning, oSuppression) and do_messages_match(oWarning, oSuppression)


def do_ids_match(oWarning, oSuppression):
    '''
    Checks if the suppression ID matches the warning ID.

    Parameters:

      oWarning : (warning object)

      oSuppression : (suppression object)

    Returns: (boolean)
    '''
    if re.fullmatch(oSuppression.get_warning_id(), oWarning.get_id()):
        return True
    return False


def do_messages_match(oWarning, oSuppression):
    '''
    Checks if the suppression message matches the warning message.

    Parameters:

      oWarning : (warning object)

      oSuppression : (suppression object)

    Returns: (boolean)
    '''
    if re.match('^.*' + oSuppression.get_message(), oWarning.get_message()):
        return True
    return False

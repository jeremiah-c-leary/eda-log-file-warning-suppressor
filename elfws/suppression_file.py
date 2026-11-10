
import re
import yaml

from elfws import error
from elfws import suppression
from elfws import suppression_list
from elfws.exit_code import ExitCode

NOT_SPECIFIED = '<None>'


def read_suppression_list(sFileName):
    dSuppression = read_suppression_file(sFileName)
    return create_suppression_list(dSuppression)


def read_suppression_file(sFileName):
    '''
    Attempts to read the suppression file and return an list of rules.

    Parameters:

       sFileName : (String)

    Returns:  dictionary
    '''
    try:
        return replace_missing_with_default(load_yaml_file(sFileName), {})
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as e:
        raise_suppression_file_error(e)


def load_yaml_file(sFileName):
    with open(sFileName) as yaml_file:
        return yaml.safe_load(yaml_file)


def raise_suppression_file_error(oError):
    raise error.ElfwsError(str(oError), ExitCode.SUPPRESSION_FILE_ERROR)


def create_suppression_list(dSuppression):
    '''
    Processes a given dictionary and returns a suppression list object.

    If any rule is malformed, every problem found is printed and the
    program exits with code 1 (suppression file error).

    Parameters:

        dSuppression : (dict)

    Returns:  suppression list object
    '''
    oExtractor = SuppressionRuleExtractor()
    lRules = oExtractor.extract_rules(dSuppression)
    raise_if_suppression_file_has_errors(oExtractor.lErrors)
    return build_suppression_list(lRules)


class SuppressionRuleExtractor():
    '''
    Extracts suppression rules from a suppression file.

    Every problem found is recorded in lErrors, so all of them can be
    reported together instead of stopping at the first one.
    '''

    def __init__(self):
        self.lErrors = []

    def extract_rules(self, dSuppression):
        if not is_mapping(dSuppression):
            self.lErrors.append('suppression file must contain a mapping with a "suppress" key')
            return []
        if not has_suppress_section(dSuppression):
            return []
        return self.search_group(dSuppression['suppress'], ['suppress'])

    def search_group(self, dGroup, lPath):
        '''
        Searches a group, and the groups nested in it, for rules keys.

        Parameters:

            dGroup : (dict)

            lPath : (list of strings) keys leading to the group, used in error messages

        Returns: list of suppression rules
        '''
        if is_missing(dGroup):
            return []
        if not is_mapping(dGroup):
            self.add_error(lPath, 'expected a group or "rules" key, found ' + repr(dGroup))
            return []

        lReturn = []
        for sKey in list(dGroup.keys()):
            lReturn.extend(self.search_key(dGroup, sKey, lPath))
        return lReturn

    def search_key(self, dGroup, sKey, lPath):
        lKeyPath = lPath + [str(sKey)]
        if is_rules_key(sKey):
            return self.extract_rules_section(dGroup[sKey], lKeyPath)
        return self.search_group(dGroup[sKey], lKeyPath)

    def extract_rules_section(self, dRules, lPath):
        if is_missing(dRules):
            return []
        if not is_mapping(dRules):
            self.add_error(lPath, 'expected warning ids, found ' + repr(dRules))
            return []

        lReturn = []
        for sId in list(dRules.keys()):
            lIdPath = lPath + [str(sId)]
            lReturn.extend(self.extract_rules_for_warning_id(sId, dRules[sId], lIdPath))
        return lReturn

    def extract_rules_for_warning_id(self, sId, lRules, lPath):
        if not is_list(lRules):
            self.add_error(lPath, 'expected a list of rules, found ' + repr(lRules))
            return []

        lReturn = []
        for iIndex, dSup in enumerate(lRules):
            lRulePath = add_index_to_path(lPath, iIndex)
            if self.validate_rule(sId, dSup, lRulePath):
                lReturn.append(create_suppression_rule(sId, dSup))
        return lReturn

    def validate_rule(self, sId, dSup, lPath):
        if not self.validate_rule_structure(dSup, lPath):
            return False
        return self.validate_rule_regular_expressions(sId, dSup, lPath)

    def validate_rule_structure(self, dSup, lPath):
        if not is_mapping(dSup):
            self.add_error(lPath, 'expected a rule with a "msg" key, found ' + repr(dSup))
            return False
        if not has_message(dSup):
            self.add_error(lPath, 'rule is missing the required "msg" key')
            return False
        return True

    def validate_rule_regular_expressions(self, sId, dSup, lPath):
        fIdValid = self.validate_regular_expression(str(sId), 'warning id', lPath)
        fMessageValid = self.validate_regular_expression(str(dSup['msg']), 'msg', lPath)
        return fIdValid and fMessageValid

    def validate_regular_expression(self, sRegex, sField, lPath):
        try:
            re.compile(sRegex)
        except re.error as e:
            self.add_error(lPath, 'invalid regular expression in ' + sField + ' ' + repr(sRegex) + ': ' + str(e))
            return False
        return True

    def add_error(self, lPath, sMessage):
        self.lErrors.append(format_path(lPath) + ': ' + sMessage)


def raise_if_suppression_file_has_errors(lErrors):
    '''
    Raises an error describing every suppression file problem, if there are any.

    Parameters:

        lErrors : (list of strings)

    Returns: Nothing
    '''
    if not has_errors(lErrors):
        return
    sMessage = format_suppression_file_errors(lErrors)
    raise error.ElfwsError(sMessage, ExitCode.SUPPRESSION_FILE_ERROR)


def format_suppression_file_errors(lErrors):
    lLines = []
    for sError in lErrors:
        lLines.append('ERROR: Suppression file: ' + sError)
    return '\n'.join(lLines)


def build_suppression_list(lRules):
    oReturn = suppression_list.SuppressionList()
    for oRule in lRules:
        oReturn.add_suppression(oRule)
    return oReturn


def create_suppression_rule(sId, dSup):
    oSupRule = suppression.Suppression(str(sId), str(dSup['msg']))
    update_suppression_author(oSupRule, dSup)
    update_suppression_comment(oSupRule, dSup)
    update_suppression_investigate(oSupRule, dSup)
    update_suppression_options(oSupRule, dSup)
    return oSupRule


def format_path(lPath):
    return ' -> '.join(lPath)


def add_index_to_path(lPath, iIndex):
    return lPath[:-1] + [lPath[-1] + '[' + str(iIndex) + ']']


def replace_missing_with_default(oValue, oDefault):
    if is_missing(oValue):
        return oDefault
    return oValue


def has_errors(lErrors):
    return len(lErrors) > 0


def has_suppress_section(dSuppression):
    return not is_missing(dSuppression.get('suppress'))


def has_message(dSup):
    return not is_missing(dSup.get('msg'))


def is_rules_key(sKey):
    return sKey == 'rules'


def is_missing(oValue):
    return oValue is None


def is_mapping(oValue):
    return isinstance(oValue, dict)


def is_list(oValue):
    return isinstance(oValue, list)


def update_suppression_author(oSupRule, dSup):
    oSupRule.author = dSup.get('author', NOT_SPECIFIED)


def update_suppression_comment(oSupRule, dSup):
    oSupRule.comment = dSup.get('comment', NOT_SPECIFIED)


def update_suppression_investigate(oSupRule, dSup):
    '''
    Updates the suppression rule based on the investigate key.

    Parameters:

        oSupRule : (suppression rule object)

        dSup : (dictionary)

    Returns: Nothing
    '''
    oSupRule.investigate = bool(dSup.get('investigate', False))


def update_suppression_options(oSupRule, dSup):
    '''
    Updates the suppression rule based on the option key.

    Parameters:

        oSupRule : (suppression rule object)

        dSup : (dictionary)

    Returns: Nothing
    '''
    oSupRule.set_options(replace_missing_with_default(dSup.get('options'), []))

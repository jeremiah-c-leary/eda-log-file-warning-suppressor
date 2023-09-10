
from elfws import warning
from elfws import warning_list

from elfws.vendor import utils as vendor_utils
from elfws.vendor.mentor_graphics import utils as cdc_utils


def get_vendor():
    return ['Mentor Graphics']


def get_tool_name():
    return 'questa_cdc'


def is_logfile(lFile):
    fToolFound = False
    for iLineNumber, sLine in enumerate(lFile):
        if fToolFound:
           if sLine.startswith('Clock Domain Crossing Analysis Report.'):
               return True
        if sLine.startswith('Questa CDC Version'):
            fToolFound = True
        if iLineNumber == 10:
            break
    return False


def extract_warnings(lFile):
    oReturn = warning_list.create()

    extract_inferred_clocks(oReturn, lFile)
    extract_inferred_resets(oReturn, lFile)
    cdc_utils.extract_cdc_violations(oReturn, lFile)
    cdc_utils.extract_cdc_cautions(oReturn, lFile)
    cdc_utils.extract_cdc_evaluations(oReturn, lFile)
    extract_design_information(oReturn, lFile)
    extract_port_domain_information(oReturn, lFile)

    return oReturn


def extract_inferred_clocks(oReturn, lFile):

    extract_inferred(oReturn, lFile, 'inferred_clock', 'Clock Group Summary for ')


def extract_inferred_resets(oReturn, lFile):

    extract_inferred(oReturn, lFile, 'inferred_reset', 'Reset Tree Summary for ')


def extract_inferred(oReturn, lFile, sID, sType):

    fWarningSectionFound = False
    for iLineNumber, sLine in enumerate(lFile):
        if sLine.startswith(sType):
            fWarningSectionFound = True

        if fWarningSectionFound:
            if sLine.startswith(' 3. Ignored'):
                fWarningSectionFound = False
                break
            if sLine.startswith(' 2. Inferred'):
                lLine = sLine.split()
                if lLine[-1] != ':(0)':
                    oWarning = warning.create(sID, sLine, None, iLineNumber + 1)
                    oReturn.add_warning(oWarning)




def extract_design_information(oReturn, lFile):
    extract_number_of_empty_modules(oReturn, lFile)
    extract_number_of_unresolved_modules(oReturn, lFile)


def extract_number_of_empty_modules(oReturn, lFile):
    check_design_element_which_must_be_zero(oReturn, lFile, 'empty_modules', 'Number of Empty Modules')


def extract_number_of_unresolved_modules(oReturn, lFile):
    check_design_element_which_must_be_zero(oReturn, lFile, 'unresolved_modules', 'Number of Unresolved Modules')


def check_design_element_which_must_be_zero(oReturn, lFile, sID, sType):

    fWarningSectionFound = False
    fTemp = False
    for iLineNumber, sLine in enumerate(lFile):
        if vendor_utils.sequence_of_lines_starts_with(iLineNumber, lFile, ['Design Information', '----']):
            fWarningSectionFound = True
            continue
        if fWarningSectionFound:
           if sLine == '':
               break
           if sLine.startswith(sType):
               lLine = sLine.split()
               if lLine[-1] != '0':
                   oWarning = warning.create(sID, sLine, None, iLineNumber + 1)
                   oReturn.add_warning(oWarning) 


def extract_port_domain_information(oReturn, lFile):
    fWarningSectionFound = False
    sID = 'non_user_defined_port_domain'
    for iLineNumber, sLine in enumerate(lFile):
        if vendor_utils.sequence_of_lines_starts_with(iLineNumber, lFile, ['Section 10 :', '====', 'Port', '----']):
            fWarningSectionFound = True
            continue
        if fWarningSectionFound:
            if sLine == '':
                break
            lLine = sLine.split()
            if lLine[-1] != 'User':
               oWarning = warning.create(sID, sLine, None, iLineNumber + 1)
               oReturn.add_warning(oWarning) 


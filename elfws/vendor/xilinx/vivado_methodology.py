from elfws import warning
from elfws import warning_list


def get_vendor():
    return ['Xilinx']


def get_tool_name():
    return 'vivado'


def is_logfile(lFile):
    bSearch = False
    for iLineNumber, sLine in enumerate(lFile):
        if 'Tool Version' in sLine and 'Vivado' in sLine:
            bSearch = True
        if bSearch and sLine.startswith('Report Methodology'):
            return True
        if iLineNumber == 200:
            return False
    return False


def extract_warnings(lFile):
    oReturn = warning_list.create()

    lRules = extract_rule_ids_from_summary(lFile)
    iNumSection = 0
    iWarningLine = 0
    for iLineNumber, sLine in enumerate(lFile):

        if iWarningLine == 0:
            for sRule in lRules:
                if sLine.startswith(sRule):
                    iWarningLine = 1
                    sID = sRule

        if iWarningLine == 1:
            iWarningLine += 1
        elif iWarningLine == 2:
            iWarningLine += 1
        elif iWarningLine == 3:
            sMessage = sLine
            iWarningLine += 1
        elif iWarningLine == 4:
            iWarningLine = 0
            oWarning = warning.create(sID, sMessage, None, iLineNumber - 2) 
            oReturn.add_warning(oWarning)

    return oReturn


def extract_rule_ids_from_summary(lFile):
    iNumSection = 0
    iTableDivider = 0
    lReturn = []
    for sLine in lFile:
        if iTableDivider == 3:
            break
        if iTableDivider == 2 and not sLine.startswith('+---'):
            lLine = sLine.split()
            lReturn.append(lLine[1])
        if iNumSection == 2 and sLine.startswith('+---'):
            iTableDivider += 1 
        if sLine.startswith('1. REPORT SUMMARY'):
            iNumSection += 1 
    return lReturn

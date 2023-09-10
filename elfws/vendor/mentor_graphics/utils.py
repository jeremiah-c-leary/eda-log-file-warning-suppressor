
from elfws import warning


def extract_cdc_violations(oReturn, lFile):

    extract_cdc_results(oReturn, lFile, 'cdc_violations', 'Violations')


def extract_cdc_cautions(oReturn, lFile):

    extract_cdc_results(oReturn, lFile, 'cdc_cautions', 'Cautions')


def extract_cdc_evaluations(oReturn, lFile):

    extract_cdc_results(oReturn, lFile, 'cdc_evaluations', 'Evaluations')


def extract_cdc_results(oReturn, lFile, sID, sType):
    fWarningSectionFound = False
    fTemp = False
    for iLineNumber, sLine in enumerate(lFile):
        if sLine.startswith('CDC Summary'):
            fWarningSectionFound = True
            continue

        if fTemp:
           if sLine.startswith('---'):
               continue
           if sLine == '':
               break
           oWarning = warning.create(sID, sLine, None, iLineNumber + 1)
           oReturn.add_warning(oWarning) 

        if fWarningSectionFound and sLine.startswith(sType):
            lLine = sLine.split()
            if lLine[-1] == '(0)':
                break
            fTemp = True
            continue


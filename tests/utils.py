

def read_file(sFilename):
    lReturn = []
    with open(sFilename) as oFile:
        for sLine in oFile:
            lReturn.append(sLine.rstrip())
    return lReturn


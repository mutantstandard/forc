


def compileNameRecords(outputFormats, nameRecords):

    compiledNameRecords = dict()

    for f in outputFormats:
        compiledNameRecords[f] = dict()

        for index, record in nameRecords['all'].items():
            compiledNameRecords[f][index] = record

        if f in nameRecords:
            for index, record in nameRecords[f].items():
                compiledNameRecords[f][index] = record

    return compiledNameRecords


def validateManifest(outputFormats, m):


    # GENERAL METADATA
    # ---------------------------------------------------
    if not m['metadata']['headVersion']:
        raise ValueError(f"You don't have a headVersion in your manifest!")



    # NAME RECORDS
    # ---------------------------------------------------
    compiledNameRecords = compileNameRecords(outputFormats, m['metadata']['nameRecords'])
    requiredNameRecords = [1,2,3,4,5,6,16,17]

    # see if the required name records are here.
    for format, formatRecords in compiledNameRecords.items():
        for f in requiredNameRecords:
            if not str(f) in formatRecords:
                raise ValueError(f"When compiled, your name records for the '{format}' format are missing a necessary name record type ({str(f)})")


    # see if version data is correct.
    for format, recordSet in compiledNameRecords.items():

        # version
        version = recordSet["5"]

        if not version.startswith("Version"):
            raise ValueError(f"The version data in the compiled name records '{format}' format is missing 'Version' at the beginning. All I see is: '{version}'.")

        if len(version.split(' ')) < 2:
            raise ValueError(f"The version data in the compiled name records for the '{format}' format is missing a number after 'Version'.")

        try:
            versionNum = float(version.split(' ')[1])
        except ValueError:
            raise ValueError(f"The version data record (type 5) for the '{format}' format is missing a number after 'Version', all I see is: '{version.split(' ')[1]}'.")

        if not versionNum == m['metadata']['headVersion']:
            raise ValueError(f"The version number in the compiled name records for the '{format}' format ('{versionNum}') is not the same as the version number for the head table ('{m['metadata']['headVersion']}').")

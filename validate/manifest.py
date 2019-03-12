


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







def validateMetadata(outputFormats, metadata):

        # HEAD VERSION
        # ---------------------------------------------------

        if not metadata['headVersion']:
            raise ValueError(f"You don't have a headVersion in your manifest!")

        try:
            float(metadata['headVersion'])
        except ValueError:
            raise ValueError(f"YOur headVersion metadata is not a number.")

        headVersionComponents = metadata['headVersion'].split('.')

        if not len(headVersionComponents[1]) == 3:
            raise ValueError(f"The version number in your headVersion needs to have 3 decimal places. The one you gave has {len(headVersionComponents[1])}.")





        # NAME RECORDS
        # ---------------------------------------------------
        compiledNameRecords = compileNameRecords(outputFormats, metadata['nameRecords'])
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

            # check if version is a number
            versionNumString = version.split(' ')[1]

            try:
                versionNum = float(versionNumString)
            except ValueError:
                raise ValueError(f"The version data record (type 5) for the '{format}' format is missing a number after 'Version', all I see is: '{version.split(' ')[1]}'.")

            # check if version is the same as headVersion.
            if not versionNumString == metadata['headVersion']:
                raise ValueError(f"The version number in the compiled name records for the '{format}' format ('{versionNum}') is not the same as the version number for the head table ('{metadata['headVersion']}').")

            versionNumComponents = versionNumString.split('.')

            if not len(versionNumComponents[1]) == 3:
                raise ValueError(f"The version number in your name records needs to have 3 decimal places. The version number in the compiled name records for the '{format}' format has {len(versionNumComponents[1])}.")







def validateManifest(outputFormats, m):

    validateMetadata(outputFormats, m['metadata'])

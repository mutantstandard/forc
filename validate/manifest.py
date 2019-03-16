


def compileNameRecords(outputFormats, nameRecords):

    compiledNameRecords = dict()

    for f in outputFormats:
        compiledNameRecords[f] = dict()

        for index, record in nameRecords['default'].items():
            compiledNameRecords[f][index] = record

        if f in nameRecords:
            for index, record in nameRecords[f].items():
                compiledNameRecords[f][index] = record

    return compiledNameRecords







def validateMetadata(outputFormats, metadata):

        # HEAD VERSION
        # ---------------------------------------------------


        if not metadata['version']:
            raise ValueError(f"You don't have a version in your manifest!")

        version = metadata['version']

        try:
            float(version)
        except ValueError:
            raise ValueError(f"Your version in your metadata is not a float number.")

        versionComponents = version.split('.')

        if not len(versionComponents[1]) == 3:
            raise ValueError(f"The version number in your headVersion needs to have 3 decimal places. The one you gave has {len(versionComponents[1])}.")

        if versionComponents[0] == "0":
            raise ValueError(f"Your font's major version (the number before the decimal place) is 0. It should be 1 or higher (certain environments act weird if you don't,)")




        # NAME RECORDS
        # ---------------------------------------------------
        compiledNameRecords = compileNameRecords(outputFormats, metadata['nameRecords'])
        requiredNameRecords = [1,2,3,4,6,16,17]

        # see if the required name records are here.
        for format, formatRecords in compiledNameRecords.items():
            for f in requiredNameRecords:
                if not str(f) in formatRecords:
                    raise ValueError(f"When compiled, your name records for the '{format}' format are missing a necessary name record type ({str(f)})")





def validateManifest(outputFormats, m):

    validateMetadata(outputFormats, m['metadata'])

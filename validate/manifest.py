from validate.data import validateOpenTypeTag, validatePostScriptName




checkDocMsg = "Check the documentation to make sure you're doing the manifest right'."

reqMetricNames =  [ "unitsPerEm"
                  , "lowestRecPPEM"

                  , "width"
                  , "height"

                  , "xMin"
                  , "xMax"
                  , "yMin"
                  , "yMax"

                  , "horiAscent"
                  , "horiDescent"
                  , "vertAscent"
                  , "vertDescent"

                  , "spaceHLength"
                  , "spaceVLength"
                  , "normalWidth"
                  , "normalLSB"
                  , "normalHeight"
                  , "normalTSB"

                  , "OS2ySubscriptXSize"
                  , "OS2ySubscriptYSize"

                  , "OS2ySubscriptXOffset"
                  , "OS2ySubscriptYOffset"

                  , "OS2ySuperscriptXSize"
                  , "OS2ySuperscriptYSize"

                  , "OS2ySuperscriptXOffset"
                  , "OS2ySuperscriptYOffset"

                  , "OS2yStrikeoutSize"
                  , "OS2yStrikeoutPosition"
                  ]


def compileNameRecords(outputFormats, nameRecords):
    """
    Creates a quick structure for the name records that can be easily searched and validated.
    """

    compiledNameRecords = dict()

    for f in outputFormats:
        compiledNameRecords[f] = dict()

        for index, record in nameRecords['default'].items():
            compiledNameRecords[f][index] = record

        if f in nameRecords:
            for index, record in nameRecords[f].items():
                compiledNameRecords[f][index] = record

    return compiledNameRecords












def validateManifest(outputFormats, m):
    """
    Validates manifest data, both at a structural and value level.

    Will raise a ValueError if anything critically non-standard has been entered by the user.
    """

    if 'metrics' not in m:
        raise ValueError(f"No metrics data found in the manifest. {checkDocMsg}")
    if 'encoding' not in m:
        raise ValueError(f"No encoding data found in the manifest. {checkDocMsg}")
    if 'metadata' not in m:
        raise ValueError(f"No metadata data found in the manifest. {checkDocMsg}")

    metrics = m['metrics']
    encoding = m['encoding']
    metadata = m['metadata']



    # METRICS
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------

    # make sure there are no excess unchecked values.
    if not len(metrics) == len(reqMetricNames):
        raise ValueError(f"You have more values than the required values than your metrics. {checkDocMsg}")

    # check for appropriate names.
    for reqName in reqMetricNames:
        if not reqName in metrics:
            raise ValueError(f"metric.{reqName} is missing from your manifest. {checkDocMsg}")

    # make sure all the values are ints.
    for name, value in metrics.items():
        if type(value) is not int:
            raise ValueError(f"metric.{name} is not an int (it's '{value}'). All of your metrics need to be formatted as ints.")




    # ENCODING
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------


    if 'macLangID' not in encoding:
        raise ValueError(f"encoding.macLangID not found in the manifest. {checkDocMsg}")
    if 'msftLangID' not in encoding:
        raise ValueError(f"encoding.msftLangID not found in the manifest. {checkDocMsg}")

    if type(encoding['macLangID']) is not str:
        raise ValueError(f"encoding.macLangID is not formatted as a string. {checkDocMsg}")
    try:
        int(encoding['macLangID'])
    except ValueError:
        raise ValueError(f"encoding.macLangID is not a string that represents a valid integer. {checkDocMsg}")



    if type(encoding['msftLangID']) is not str:
        raise ValueError(f"encoding.msftLangID is not formatted as a string. {checkDocMsg}")
    try:
        int(encoding['msftLangID'], 16)
    except ValueError:
        raise ValueError(f"encoding.msftLangID is not a string that represents a valid hexadecimal number. {checkDocMsg}")




    # METADATA
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------


    # Font Version
    # ---------------------------------------------------
    if not "version" in metadata:
        raise ValueError(f"You don't have a metadata.version in your manifest. It has to have this.")

    version = metadata['version']

    if type(metadata["version"]) is not str:
        raise ValueError(f"metadata.version is not formatted as a string. It needs to be formatted as a string.")

    try:
        float(version)
    except ValueError:
        raise ValueError(f"metadata.version is not a number that has 3 decimal places. It needs to have 3 decimal places.")

    versionComponents = version.split('.')

    if not len(versionComponents[1]) == 3:
        raise ValueError(f"metadata.version needs to have 3 decimal places. The one you gave has {len(versionComponents[1])}.")

    if versionComponents[0] == "0":
        raise ValueError(f"metadata.version is not correct. The Major Version (the number before the decimal place) is 0. It should be 1 or higher. Certain environments act weird if you don't. If you need to mark it as a beta, consider marking at such in the version notes in the manifest.")



    # OS2VendorID
    # ---------------------------------------------------
    if 'OS2VendorID' in metadata:
        try:
            validateOpenTypeTag(metadata['OS2VendorID'])
        except ValueError as e:
            raise ValueError(f"metadata.OS2VendorID doesn't conform to it's data type correctly. → {e}")


    # Filenames
    # ---------------------------------------------------

    # filenames are currently optional.
    # if the user doesn't set filenames, forc will just use the format name for the filename.
    if "filenames" in metadata:
        filenames = metadata['filenames']

        # make sure they are set.
        for format in outputFormats:
            if not format in filenames:
                raise ValueError(f"You haven't set a filename for your font for the {format} format in metadata.filenames. {checkDocMsg}")

        # check for duplicate filenames.
        for format1, filename1 in filenames.items():
            for format2, filename2 in filenames.items():
                if format2 != format1:
                    if filename1 == filename2:
                        raise ValueError(f" The filenames you've set for the formats {format1} and {format2} are the same. There can't be any duplicates in your custom filenames.")

    # Name Records
    # ---------------------------------------------------
    if not "nameRecords" in metadata:
        raise ValueError(f"There is no metadata.nameRecords. Your manifest has to have this.")

    compiledNameRecords = compileNameRecords(outputFormats, metadata['nameRecords'])
    requiredNameRecords = [1,2,3,4,6,16,17]

    # make sure all keys and values are strings.
    for format, formatRecords in compiledNameRecords.items():
        if type(format) is not str:
            raise ValueError(f"The format '{format}' in your metadata.nameRecords is not a string.")

        for key, record in formatRecords.items():
            if type(key) is not str:
                raise ValueError(f"There's a problem with metadata.nameRecords. The name record key '{key}' that corresponds to the format '{format}' is not a string.")

            try:
                int(key)
            except ValueError:
                raise ValueError(f"There's a problem with metadata.nameRecords. The name record key '{key}' that corresponds to the format '{format}' is not a string that represents a valid integer.")

            if int(key) > 25:
                raise ValueError(f"There's a problem with metadata.nameRecords. The name record key '{key}' that corresponds to the format '{format}' represents an integer that is not between 0 and 25. It must be between 0 and 25.")

            if type(record) is not str:
                raise ValueError(f"There's a problem with metadata.nameRecords. The name record '{record}' for the key {key} that corresponds to the format '{format}' is not a string.")



    # see if the required name records are here.
    for format, formatRecords in compiledNameRecords.items():
        for f in requiredNameRecords:
            if not str(f) in formatRecords:
                raise ValueError(f"There's something wrong with metadata.nameRecords. When compiled, your name records for the '{format}' format are missing a necessary name record type ({str(f)})")


    # PostScript Names
    for format, formatRecords in compiledNameRecords.items():
        try:
            validatePostScriptName(formatRecords["6"])
        except ValueError as e:
            raise ValueError(f"There's something wrong with metadata.nameRecords. When compiled, name record 6 for the '{format}' format doesn't match the data type requirements. {e}")

from data import tag, fixed
from validate.data import validatePostScriptName



checkDocMsg = "Check the documentation to make sure you're doing the manifest right'."


def compileNameRecords(nameRecords, outputFormats):
    """
    Creates a quick structure for the name records for searching and validation.
    """

    compiledNameRecords = dict()

    # make a dict for each format the user is exporting to.
    for f in outputFormats:
        compiledNameRecords[f] = dict()

        # create initial round of records based on default.
        for index, record in nameRecords['default'].items():
            compiledNameRecords[f][index] = record

        # overwrite that initial round if there are specific overlapping
        # name records for this format.
        if f in nameRecords:
            for index, record in nameRecords[f].items():
                compiledNameRecords[f][index] = record

    return compiledNameRecords




def compileFinalNameRecords(compiledNameRecords, version):
    """
    Compiles a final name record package for data by applying version data according to guidelines.
    """

    for format, records in compiledNameRecords.items():
        if "5" in records:
            records["5"] = "Version " + str(version) + " " + records["5"]
        else:
            records["5"] = "Version " + str(version)

    return compiledNameRecords





def checkTransformMetadata(metadata, outputFormats):
    """
    Checks and transforms manifest metadata, ready for font assembly.
    """

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

    metadata['version'] = fixed(metadata['version'])



    # OS2VendorID
    # ---------------------------------------------------
    if 'OS2VendorID' in metadata:
        try:
            # try to overwrite the string version with a tag data type version.
            metadata['OS2VendorID'] = tag(metadata['OS2VendorID'])
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

    compiledNameRecords = compileNameRecords(metadata['nameRecords'], outputFormats)
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




    metadata['nameRecords'] = compileFinalNameRecords(compiledNameRecords, metadata['version'])

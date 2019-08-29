

def checkTransformEncoding(encoding):

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
        # try to convert to int
        encoding['macLangID'] = int(encoding['macLangID'])
    except ValueError:
        raise ValueError(f"encoding.macLangID is not a string that represents a valid integer. {checkDocMsg}")



    if type(encoding['msftLangID']) is not str:
        raise ValueError(f"encoding.msftLangID is not formatted as a string. {checkDocMsg}")
    try:
        # try to convert to int
        encoding['msftLangID'] = int(encoding['msftLangID'], 16)
    except ValueError:
        raise ValueError(f"encoding.msftLangID is not a string that represents a valid hexadecimal number. {checkDocMsg}")

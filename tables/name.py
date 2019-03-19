from lxml.etree import Element




def makeVersionRecord(m, record=None):
    if record:
        return "Version " + m['metadata']['version'] + " " + record
    else:
        return "Version " + m['metadata']['version']


def create(format, m):
    """
    Creates a name table. Iterates over nameRecords data multiple times
    so that it's prepared in each of the name record encoding
    platforms/methods (Unicode, Macintosh, Microsoft).
    """

    macLangID = m['encoding']['macLangID']
    msftLangID = m['encoding']['msftLangID']

    # data compilation
    # -------------------------------------------------------------------

    nameRecords = m['metadata']['nameRecords']
    compiledNameRecords = {}


    # create a version record anyway if the user hasn't made version notes.
    if not "5" in nameRecords.items():
        compiledNameRecords["5"] = makeVersionRecord(m)


    # compile records based on what's in the 'all' category.
    for index, record in nameRecords['default'].items():
        if index == "5":
            compiledNameRecords[index] = makeVersionRecord(m, record)
        else:
            compiledNameRecords[index] = record


    # compile records based on what records have been set for this format.
    # This overrides anything that has already been set in 'all'.
    if format in nameRecords:
        for index, record in nameRecords[format].items():
            if index == "5":
                compiledNameRecords[index] = makeVersionRecord(m, record)
            else:
                compiledNameRecords[index] = record



    # table compilation
    # -------------------------------------------------------------------


    name = Element("name")

    # these are being repeated in this way because it's easier to read the result - that's it.

    # unicode
    for id, value in compiledNameRecords.items():
        record = Element("namerecord",  { "nameID" : id
                                        , "platformID" : "0"
                                        , "platEncID" : "0"
                                        , "langID" : "0x0"
                                        })
        record.text = value
        name.append(record)


    # macintosh
    for id, value in compiledNameRecords.items():
        record = Element("namerecord",  { "nameID" : id
                                        , "platformID" : "1"
                                        , "platEncID" : "0"
                                        , "langID" : macLangID
                                        })
        record.text = value
        name.append(record)


    # microsoft
    for id, value in compiledNameRecords.items():
        record = Element("namerecord",  { "nameID" : id
                                        , "platformID" : "3"
                                        , "platEncID" : "1"
                                        , "langID" : msftLangID
                                        })
        record.text = value
        name.append(record)



    # if the Microsoft Language ID is not American English (0x409),
    # make an additional entry with the PostScript name for American English.
    #
    # (this makes Microsoft's font validator happy)



    if int(msftLangID, 16) != int('0x0409', 16):
        americanMsftPostScript = Element("namerecord", { "nameID" : "6"
                                          , "platformID" : "3"
                                          , "platEncID" : "1"
                                          , "langID" : "0x0409"
                                          })
        americanMsftPostScript.text = compiledNameRecords["6"]
        name.append(americanMsftPostScript)


    return name

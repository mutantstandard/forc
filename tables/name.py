from lxml.etree import Element

def name(format, macLangID, msftLangID, nameRecords):
    """
    Creates a name table. Iterates over nameRecords data multiple times
    so that it's prepared in each of the name record encoding
    platforms/methods (Unicode, Macintosh, Microsoft).
    """

    # compile the name records used for this particular font.
    # take from the 'all' dict first
    # then add and overwrite withe format specific records dict.


    compiledNameRecords = {}

    for index, record in nameRecords['all'].items():
        compiledNameRecords[index] = record

    if format in nameRecords:
        for index, record in nameRecords[format].items():
            compiledNameRecords[index] = record




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

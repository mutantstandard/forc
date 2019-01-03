from xml.etree.ElementTree import Element

def name(nameRecords, macLangID, msftLangID):
    """
    Creates a name table. Iterates over nameRecords data multiple times
    so that it's prepared in each of the name record encoding
    platforms/methods (Unicode, Macintosh, Microsoft).
    """

    name = Element("name")

    # these are being repeated in this way because it's easier to read the result - that's it.

    # unicode
    for id, value in nameRecords.items():
        record = Element("namerecord",  { "nameID" : id
                                        , "platformID" : "0"
                                        , "platEncID" : "0"
                                        , "langID" : "0x0"
                                        })
        record.text = value
        name.append(record)

    # macintosh
    for id, value in nameRecords.items():
        record = Element("namerecord",  { "nameID" : id
                                        , "platformID" : "1"
                                        , "platEncID" : "0"
                                        , "langID" : macLangID
                                        })
        record.text = value
        name.append(record)

    # microsoft
    for id, value in nameRecords.items():
        record = Element("namerecord",  { "nameID" : id
                                        , "platformID" : "3"
                                        , "platEncID" : "1"
                                        , "langID" : msftLangID
                                        })
        record.text = value
        name.append(record)

    return name

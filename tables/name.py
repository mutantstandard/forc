from lxml.etree import Element

from transform.bytes import padTableBytes



class nameRecord:
    """
    Class representing a record in a name table.
    """

    def __init__(self, nameID, platformID, encodingID, languageID, text):

        self.nameID  = nameID
        self.platformID = platformID
        self.encodingID = encodingID
        self.languageID = languageID
        self.text = text


    def toTTX(self):
        record = Element("namerecord",  { "nameID" : str(self.nameID)
                                        , "platformID" : str(self.platformID)
                                        , "platEncID" : str(self.encodingID)
                                        , "langID" : str(self.languageID)
                                        })
        record.text = self.text
        return record

    # TODO: convert a nameRecord to bytes.





class name:
    """
    Class representing a name table.
    """

    def __init__(self, fontFormat, m):

        self.tableName = "name" # hard-coded. For font generation only.
        self.format = 1 # the format that is being worked with.
        self.nameRecords = []


        # data compilation
        # -------------------------------------------------------------------
        nameRecords = m['metadata']['nameRecords'][fontFormat]
        macLangID = m['encoding']['macLangID']
        msftLangID = m['encoding']['msftLangID']

        for id, value in nameRecords.items():
            self.nameRecords.append(nameRecord(int(id), 0, 0, 0x0, value)) # unicode
            self.nameRecords.append(nameRecord(int(id), 1, 0, macLangID, value)) # macintosh
            self.nameRecords.append(nameRecord(int(id), 3, 1, msftLangID, value)) # microsoft



        # if the Microsoft Language ID is not American English (0x409),
        # make an additional entry with the PostScript name for American English.
        #
        # (this makes Microsoft's font validator happy)
        if int(msftLangID, 16) != int('0x0409', 16):
            self.nameRecords.append(nameRecord(6, 3, 1, 0x0409, nameRecords["6"]))




    def toTTX(self):
        name = Element("name")

        for r in self.nameRecords:
            name.append(r.toTTX())

        return name

    def toBytes(self):
        return padTableBytes(b'\0') # placeholder

    # TODO: figure out how to compile name to bytes.

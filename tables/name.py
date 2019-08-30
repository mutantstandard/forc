import struct

from lxml.etree import Element
from transform.bytes import generateOffsets, outputTableBytes


class LangTagRecord:
    """
    Class representing a LangTagRecord in a name table.

    Only used for bytes compilation.
    """

    def __init__(self, length, offset):
        self.length = length
        self.offset = offset

    def toBytes(self):
        return struct.pack(">HH", self.length, self.offset)



class nameRecord:
    """
    Class representing a record in a name table.
    """

    def __init__(self, nameID, platformID, platEncID, languageID, text):

        self.nameID  = nameID
        self.platformID = platformID
        self.platEncID = platEncID
        self.languageID = languageID
        self.text = text


    def toTTX(self):

        languageID = ""

        if self.platformID == 1: # Mac
            languageID = str(self.languageID)
        elif self.platformID == 3: # Win
            languageID = hex(self.languageID)
        elif self.platformID == 0: # Unicode
            languageID = str(self.languageID)

        record = Element("namerecord",  { "nameID" : str(self.nameID)
                                        , "platformID" : str(self.platformID)
                                        , "platEncID" : str(self.platEncID)
                                        , "langID" : str(languageID)
                                        })
        record.text = self.text
        return record




class name:
    """
    Class representing a name table.
    """

    def __init__(self, fontFormat, m):

        self.format = 0 # the format that is being worked with.
        self.nameRecords = []


        # data compilation
        # -------------------------------------------------------------------
        nameRecords = m['metadata']['nameRecords'][fontFormat]
        macLangID = m['encoding']['macLangID']
        msftLangID = m['encoding']['msftLangID']

        for id, value in nameRecords.items():
            self.nameRecords.append(nameRecord(int(id), 0, 4, 0x0, value)) # unicode
            self.nameRecords.append(nameRecord(int(id), 1, 0, macLangID, value)) # macintosh
            self.nameRecords.append(nameRecord(int(id), 3, 1, msftLangID, value)) # microsoft



        # if the Microsoft Language ID is not American English (0x409),
        # make an additional entry with the PostScript name for American English.
        #
        # (this makes Microsoft's font validator happy)
        if msftLangID != int('0x0409', 16):
            self.nameRecords.append(nameRecord(6, 3, 1, 0x0409, nameRecords["6"]))




    def toTTX(self):
        name = Element("name")

        for r in self.nameRecords:
            name.append(r.toTTX())

        return name


    def toBytes(self):
        # This follows the structure of naming table format 0.
        # (there's a difference)


        metadata = []
        texts = []

        for nr in self.nameRecords:
            # plat 0 (Uni), platEncID any - UTF-16 encoding
            # plat 1 (Mac), assume UTF-16.
            # plat 3 (Msft), platEncID 1 - UTF-16BE encoding
            # basically just assuming UTF-16BE.

            texts.append(nr.text.encode('utf_16_be'))
            metadata.append(nr)





        stringOffset = 6 + (16*len(self.nameRecords)) + 2
        offsets = generateOffsets(texts, 16, stringOffset, usingClasses=False)

        stringData = offsets["bytes"]
        nameRecords = b''

        for num, nr in enumerate(self.nameRecords):
            nameRecords += struct.pack(">HHHHHH"
                                , nr.platformID # UInt16
                                , nr.platEncID # UInt16
                                , nr.languageID # UInt16
                                , nr.nameID # UInt16
                                , len(texts[num]) # UInt16
                                , offsets["offsetInts"][num] # Offset16 (UInt16)
                                )


        beginning = struct.pack(">HHH"
                            , self.format # UInt16
                            , len(self.nameRecords) # UInt16
                            , stringOffset # Offset16 (UInt16)
                            )



        table = beginning + nameRecords + stringData

        return outputTableBytes(table)

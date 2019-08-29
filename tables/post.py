import struct
from lxml.etree import Element
from data import Fixed, VFixed
from transform.bytes import outputTableBytes


class post:
    """
    Class representing a post table.
    """

    def __init__(self, glyphs):

        self.version = VFixed('2.0')
        # Apple suggests against using formats 2.5, 3 and 4.
        # Microsoft says that version 2.5 is depreciated.

        self.italicAngle = Fixed('0.0') # hard-coded (this is an emoji font; no italics here.)

        self.underlinePosition = 0
        self.underlineThickness = 0

        self.isFixedPitch = 1 # hard-coded

        self.minMemType42 = 0 # hard-coded
        self.maxMemType42 = 0 # hard-coded
        self.minMemType1 = 1 # hard-coded
        self.maxMemType1 = 1 # hard-coded

        self.numGlyphs = len(glyphs["img_empty"])

        # TODO: glyphNameIndex[numGlyphs]
        # TODO: names[numberNewGlyphs]

        self.extraNames = [] # this array pleases macOS.

        for g in glyphs["img_empty"]:
            self.extraNames.append(g)


    def toTTX(self):
        post.append(Element("formatType", {'value': self.version.toDecimalStr() })) # TTX wants this particular format.
        post.append(Element("italicAngle", {'value': str(self.italicAngle) }))

        post.append(Element("underlinePosition", {'value': str(self.underlinePosition) }))
        post.append(Element("underlineThickness", {'value': str(self.underlineThickness) }))

        post.append(Element("isFixedPitch", {'value': str(self.isFixedPitch) }))

        post.append(Element("minMemType42", {'value': str(self.minMemType42) }))
        post.append(Element("maxMemType42", {'value': str(self.maxMemType42) }))
        post.append(Element("minMemType1", {'value': str(self.minMemType1) }))
        post.append(Element("maxMemType1", {'value': str(self.maxMemType1) }))

        post.append(Element("psNames")) # TODO: dunno what this is represented by.


        # extraNames to please macOS.
        extraNames = Element("extraNames")
        for g in self.extraNames:
            extraNames.append(Element("psName", {"name": g.name() }))

        post.append(extraNames)

        return post


    def toBytes(self):
        post = struct.pack( ">iihhIIIIIH"
                          , int(self.version) # Fixed, version no. type (Int32)
                          , int(self.italicAngle) # Fixed (Int32)

                          , self.underlinePosition # FWORD (Int16)
                          , self.underlineThickness # FWORD (Int16)

                          , self.isFixedPitch # UInt32
                          , self.minMemType42 # UInt32
                          , self.maxMemType42 # UInt32
                          , self.minMemType1 # UInt32
                          , self.maxMemType1 # UInt32

                          , self.numGlyphs # UInt16
                          )

        return outputTableBytes(post)

        # TODO: append self.extraNames
        # details about extraNames (names) - https://docs.microsoft.com/en-gb/typography/opentype/spec/post#version-20

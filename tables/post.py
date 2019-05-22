from lxml.etree import Element
from data import fixed, vFixed


class post:
    """
    Class representing a post table.
    """

    def __init__(self, glyphs):

        self.version = vFixed('2.0')
        # Apple suggests against using formats 2.5, 3 and 4.
        # Microsoft says that version 2.5 is depreciated.

        self.italicAngle = fixed('0.0')

        self.underlinePosition = 0
        self.underlineThickness = 0

        self.isFixedPitch = 1

        self.minMemType42 = 0
        self.maxMemType42 = 0
        self.minMemType1 = 1
        self.maxMemType1 = 1

        self.extraNames = [] # this array pleases macOS.

        for g in glyphs["img_empty"]:
            self.extraNames.append(g)



    def toTTX(self):
        post = Element("post")

        post.append(Element("formatType", {'value': self.version.toDecimalStr() })) # TTX wants a decimal string version of this.
        post.append(Element("italicAngle", {'value': str(self.italicAngle) })) # hard-coded

        post.append(Element("underlinePosition", {'value': str(self.underlinePosition) }))
        post.append(Element("underlineThickness", {'value': str(self.underlineThickness) }))

        post.append(Element("isFixedPitch", {'value': str(self.isFixedPitch) })) # hard-coded

        post.append(Element("minMemType42", {'value': str(self.minMemType42) })) # hard-coded
        post.append(Element("maxMemType42", {'value': str(self.maxMemType42) })) # hard-coded
        post.append(Element("minMemType1", {'value': str(self.minMemType1) })) # hard-coded
        post.append(Element("maxMemType1", {'value': str(self.maxMemType1) })) # hard-coded

        post.append(Element("psNames")) # dunno what this is represented by.


        # extraNames to please macOS.
        extraNames = Element("extraNames")
        for g in self.extraNames:
            extraNames.append(Element("psName", {"name": g.name() }))

        post.append(extraNames)

        return post


    def toBytes(self):
        return struct.pack( ">iihhIIIII"
                          , int(self.version) # Fixed, version no. type (Int32)
                          , int(self.italicAngle) # Fixed (Int32)

                          , self.underlinePosition # FWORD (Int16)
                          , self.underlineThickness # FWORD (Int16)

                          , self.isFixedPitch # UInt32
                          , self.minMemType42 # UInt32
                          , self.maxMemType42 # UInt32
                          , self.minMemType1 # UInt32
                          , self.maxMemType1 # UInt32

                          # self.extraNames # TODO: where the glyphs at???
                          )

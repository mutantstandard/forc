from lxml.etree import Element



class post:
    """
    Class representing a post table.
    """

    def __init__(self, glyphs):
        self.version = 0x0002000 # binary version
        self.versionTTX = '2.0' # TODO: merge with normal version. Probably by converting it to some kind of fixed.
        # Apple suggests against using formats 2.5, 3 and 4.

        self.italicAngle = 0.0

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

        post.append(Element("formatType", {'value': self.versionTTX })) # hard-coded,
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

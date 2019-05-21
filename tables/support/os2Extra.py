import struct
from lxml.etree import Element

class panose:
    """
    Class representing the PANOSE segment of an OS/2 table.
    """

    def __init__(self
                , bFamilyType
                , bSerifStyle
                , bWeight
                , bProportion
                , bContrast
                , bStrokeVariation
                , bArmStyle
                , bLetterForm
                , bMidline
                , bXHeight
                ):

        # these are all hard-coded to be the optimal values for an emoji font.
        self.bFamilyType = bFamilyType
        self.bSerifStyle = bSerifStyle
        self.bWeight = bWeight
        self.bProportion = bProportion
        self.bContrast = bContrast
        self.bStrokeVariation = bStrokeVariation
        self.bArmStyle = bArmStyle
        self.bLetterForm = bLetterForm
        self.bMidline = bMidline
        self.bXHeight = bXHeight



    def toTTX(self):
        panose = Element("panose")
        panose.append(Element("bFamilyType", {'value': str(self.bFamilyType) }))
        panose.append(Element("bSerifStyle", {'value': str(self.bSerifStyle) }))
        panose.append(Element("bWeight", {'value': str(self.bWeight) }))
        panose.append(Element("bProportion", {'value': str(self.bProportion) }))
        panose.append(Element("bContrast", {'value': str(self.bContrast) }))
        panose.append(Element("bStrokeVariation", {'value': str(self.bStrokeVariation) }))
        panose.append(Element("bArmStyle", {'value': str(self.bArmStyle) }))
        panose.append(Element("bLetterForm", {'value': str(self.bLetterForm) }))
        panose.append(Element("bMidline", {'value': str(self.bMidline) }))
        panose.append(Element("bXHeight", {'value': str(self.bXHeight) }))

        return panose


        
    def toBinary(self):
        return struct.pack(">HHHHHHHHHH"
                          , self.bFamilyType
                          , self.bSerifStyle
                          , self.bWeight
                          , self.bProportion
                          , self.bContrast
                          , self.bStrokeVariation
                          , self.bArmStyle
                          , self.bLetterForm
                          , self.bMidline
                          , self.bXHeight
                          )

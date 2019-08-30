from lxml.etree import Element
import struct

from data import VFixed
from transform.bytes import outputTableBytes

class maxp:
    def __init__(self, glyphs):

        self.version = VFixed('1.0') # hard-coded

        self.numGlyphs = len(glyphs["all"])
        # sbix determines the number of glyphs from this data point.

        self.maxPoints = 0
        self.maxContours = 0
        self.maxCompositePoints = 0
        self.maxCompositeContours = 0

        self.maxZones = 0
        self.maxTwilightPoints = 0

        self.maxStorage = 1
        self.maxFunctionDefs = 1
        self.maxInstructionDefs = 0
        self.maxStackElements = 64

        self.maxSizeOfInstructions = 0
        self.maxComponentElements = 0
        self.maxComponentDepth = 0



    def toTTX(self):
        # TTX re-calculates most, if not all of these values by itself, but it's still worth giving them anyway.

        maxp = Element("maxp")

        maxp.append(Element("tableVersion", {'value': self.version.toHexStr() })) # TTX wants the version in this format.

        maxp.append(Element("numGlyphs", {'value': str(self.numGlyphs) })) # TTX re-calculates this, but I'm giving it the right value anyway.

        maxp.append(Element("maxPoints", {'value': str(self.maxPoints) }))
        maxp.append(Element("maxContours", {'value': str(self.maxContours) }))
        maxp.append(Element("maxCompositePoints", {'value': str(self.maxCompositePoints) }))
        maxp.append(Element("maxCompositeContours", {'value': str(self.maxCompositeContours) }))

        maxp.append(Element("maxZones", {'value': str(self.maxZones) }))
        maxp.append(Element("maxTwilightPoints", {'value': str(self.maxTwilightPoints) }))

        maxp.append(Element("maxStorage", {'value': str(self.maxStorage) }))
        maxp.append(Element("maxFunctionDefs", {'value': str(self.maxFunctionDefs) }))
        maxp.append(Element("maxInstructionDefs", {'value': str(self.maxInstructionDefs) }))
        maxp.append(Element("maxStackElements", {'value': str(self.maxStackElements) }))

        maxp.append(Element("maxSizeOfInstructions", {'value': str(self.maxSizeOfInstructions) }))
        maxp.append(Element("maxComponentElements", {'value': str(self.maxComponentElements) }))
        maxp.append(Element("maxComponentDepth", {'value': str(self.maxComponentDepth) }))

        return maxp



    def toBytes(self):
        maxp = struct.pack( ">iHHHHHHHHHHHHHH"
                          , int(self.version) # Fixed (Int32)

                          , self.numGlyphs # UInt16

                          , self.maxPoints # UInt16
                          , self.maxContours # UInt16
                          , self.maxCompositePoints # UInt16
                          , self.maxCompositeContours # UInt16

                          , self.maxZones # UInt16
                          , self.maxTwilightPoints # UInt16

                          , self.maxStorage # UInt16
                          , self.maxFunctionDefs # UInt16
                          , self.maxInstructionDefs # UInt16
                          , self.maxStackElements # UInt16

                          , self.maxSizeOfInstructions # UInt16
                          , self.maxComponentElements # UInt16
                          , self.maxComponentDepth # UInt16
                          )

        return outputTableBytes(maxp)

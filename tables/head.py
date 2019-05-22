import struct
from lxml.etree import Element

from data import bFlags, longDateTime

class head:
    """
    Class representing a 'head' table.
    """

    def __init__(self, m):

        self.majorVersion = 1 # hard-coded, is meant to be 1.
        self.minorVersion = 0 # hard-coded, is meant to be 0.
        self.fontRevision = m['metadata']['version'] # fixed format.

        self.checkSumAdjustment = 0 # this is only set at compilation.
        self.magicNumber = 0x5f0f3cf5 # hard-coded

        self.flags = bFlags('11010000 00000000') # hard-coded
        self.unitsPerEm = m['metrics']['unitsPerEm']

        self.created = m['metadata']['created'] # (is a longDateTime)
        self.modified = longDateTime() # is set to 'now'

        self.xMin = m['metrics']['xMin']
        self.yMin = m['metrics']['yMin']
        self.xMax = m['metrics']['xMax']
        self.yMax = m['metrics']['yMax']

        self.macStyle = bFlags('00000000 00000000') # hard-coded. Must agree with OS/2's fsType.
        self.lowestRecPPEM = m['metrics']['lowestRecPPEM']

        self.fontDirectionHint = 2 # depreciated; is meant to be 2.
        self.indexToLocFormat = 0 # This determines the format of the loca table.
        self.glyphDataFormat = 0 # not important, hard-coded





    def toTTX(self):
        """
        Compiles table to TTX.
        """

        head = Element("head")

        head.append(Element("tableVersion", {'value': str(self.majorVersion) + '.' + str(self.minorVersion)  }))
        head.append(Element("fontRevision", {'value': str(self.fontRevision) })) # TTX is weird about font versioning, only accepts a basic string, so use str.

        head.append(Element("checkSumAdjustment", {'value': str(self.checkSumAdjustment) })) # TTX changes this at compilation, so we don't need to bother with this for this compiler.
        head.append(Element("magicNumber", {'value': hex(self.magicNumber) }))

        head.append(Element("flags", {'value': self.flags.toTTXStr() }))
        head.append(Element("unitsPerEm", {'value': str( self.unitsPerEm )}))

        head.append(Element("created", {'value':  self.created.toTTXStr() }))
        head.append(Element("modified", {'value': self.modified.toTTXStr() })) # TTX eats the value given and creates it's own date at compilation *shrugs*

        head.append(Element("xMin", {'value': str(self.xMin) }))
        head.append(Element("yMin", {'value': str(self.yMin) }))
        head.append(Element("xMax", {'value': str(self.xMax) }))
        head.append(Element("yMax", {'value': str(self.yMax) }))

        head.append(Element("macStyle", {'value': self.macStyle.toTTXStr() }))
        head.append(Element("lowestRecPPEM", {'value': str(self.lowestRecPPEM) }))

        head.append(Element("fontDirectionHint", {'value': str(self.fontDirectionHint) }))
        head.append(Element("indexToLocFormat", {'value': str(self.indexToLocFormat) }))
        head.append(Element("glyphDataFormat", {'value': str(self.glyphDataFormat) }))

        return head



    def toBytes(self):
        return struct.pack( '>HHiII2bHqqhhhh2bHhhh'

                            , self.majorVersion # UInt16
                            , self.minorVersion # UInt16
                            , int(self.fontRevision) # Fixed (Int32 but fixed-point)

                            , self.checksumAdjustment # UInt32
                            , self.magicNumber # UInt32

                            , self.flags.toBytes() # 2 bytes/UInt16
                            , self.unitsPerEm # UInt16

                            , int(self.created) # LONGDATETIME (Int64)
                            , int(self.modified) # LONGDATETIME (Int64)

                            , self.xMin # Int16
                            , self.yMin # Int16
                            , self.xMax # Int16
                            , self.yMax # Int16

                            , self.macStyle.toBytes() # 2 bytes/UInt16
                            , self.lowerstRecPPEM # UInt16

                            , self.fontDirectionHint # Int16
                            , self.indexToLocFormat # Int16
                            , self.glyphDataFormat # Int16
                            )

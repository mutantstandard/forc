import struct
from lxml.etree import Element
from transform.bytes import padTableBytes

class GaspRange:
    """
    Class representing a placeholder GaspRange record.
    """

    def __init__(self):
        self.rangeMaxPPEM = 65535
        self.rangeGaspBehavior = 0x0f

    def toTTX(self):
        return Element("gaspRange", {'rangeMaxPPEM': str(self.rangeMaxPPEM) # Decimal string
                                     ,'rangeGaspBehavior': hex(self.rangeGaspBehavior) # Hex string
                                     })
    def toBytes(self):
        return struct.pack( ">HH"
                          , self.rangeMaxPPEM # UInt16
                          , self.rangeGaspBehavior # UInt16
                          )

class gasp:
    """
    Class representing a really basic gasp table.
    """

    def __init__(self):
        self.tableName = "gasp" # hard-coded.  For font generation only.

        self.version = 1
        self.gaspRanges = []
        self.gaspRanges.append(GaspRange())


    def toTTX(self):
        gasp = Element("gasp")

        # - TTX doesnt have version for gasp table.

        for gr in self.gaspRanges:
            gasp.append(gr.toTTX())

        return gasp


    def toBytes(self):
        gasp = struct.pack( ">HH"
                          , self.version # UInt16
                          , len(self.gaspRanges) # UInt16 (numRanges)
                          )

        for gr in self.gaspRanges:
            gasp += gr.toBytes()

        return padTableBytes(gasp)

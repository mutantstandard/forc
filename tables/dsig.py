import struct
from lxml.etree import Element

from data import BFlags
from transform.bytes import padTableBytes

class DSIG:
    """
    Class representing a placeholder DSIG table.
    """

    def __init__(self):

        self.tableName = "DSIG" # hard-coded.  For font generation only.

        self.version = 0x00000001
        # Hardcoded. It is what it's supposed to be - a single UInt32 formatted as hex.

        self.flags = BFlags('00000000')
        self.numSigs = 0


    def toTTX(self):
        """
        Create a dummy DSIG table.
        """

        dsig = Element("DSIG")

        dsig.append(Element("tableHeader", {'version': hex(self.version)
                                           ,'flag': self.flags.toTTXStr()
                                           ,'numSigs': str(self.numSigs)
                                           }))

        return dsig

    def toBytes(self):
        dsig = struct.pack( '>I2sH'
                          , self.version # UInt32 (not fixed type!)
                          , self.flags.toBytes() # 2 bytes/UInt16
                          , self.numSigs # UInt16
                          )

        return padTableBytes(dsig)

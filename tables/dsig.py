import struct
from lxml.etree import Element

from data import bFlags

class dsig:
    """
    Class representing a placeholder DSIG table.
    """

    def __init__(self):

        self.version = 0x00000001
        # Hardcoded. It is what it's supposed to be - a single UInt32.

        self.flags = bFlags('00000000')
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

    def toBinary(self):
        return struct.pack( '>IHH'
                          , self.version # UInt32 (not fixed!)
                          , self.flag # UInt16
                          , self.numSigs # UInt16
                          )

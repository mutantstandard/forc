from data import Tag
import struct

class TableRecord:
    """
    Simple class representing a single Table Record in a font.
    """
    def __init__(self, tag, checkSum, offset, length):

        try:
            self.tag = Tag(tag)
        except ValueError as e:
            raise ValueError(f"Creating tableRecord failed. -> {e}")

        self.checkSum = checkSum
        self.offset = offset
        self.length = length

    def toBytes(self):
        return struct.pack (">4sHHH"
                           , self.tag.toBytes() # 4 bytes (UInt32)
                           , self.checkSum # UInt32
                           , self.offset # UInt32 (Offset32)
                           , self.length # UInt32
                           )

    def __lt__(self, other):
        if int(self.tag) < int(other.tag):
            return True
        else:
            return False

from data import Tag
import struct

class TableRecord:
    """
    Simple class representing a single Table Record in a font.

    These are only relevant for bytes compilation, so there's no TTX output.
    """
    def __init__(self, tag, checkSum, offset, length):

        try:
            self.tag = Tag(tag)
        except ValueError as e:
            raise ValueError(f"Creating tableRecord failed. -> {e}")

        self.checkSum = checkSum
        self.offset = offset # from the very beginning of the TrueType file.
        self.length = length

    def toBytes(self):
        return struct.pack (">4sIII"
                           , self.tag.toBytes() # 4 bytes (UInt32)
                           , self.checkSum # UInt32
                           , self.offset # UInt32 (Offset32)
                           , self.length # UInt32
                           )

        # this is not a normal table, and thus should not be padded.

    def __lt__(self, other):
        """
        Required because TableRecords need to be sorted from lowest
        to highest tag value when in use in an actual font file.
        """
        if int(self.tag) < int(other.tag):
            return True
        else:
            return False

    def __repr__(self):
        return f"TableRecord for {self.tag} - offset: {self.offset} - length: {self.length}\n"

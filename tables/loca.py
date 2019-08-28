from lxml.etree import Element

from transform.bytes import padTableBytes

class loca:
    """
    Class representing a placeholder loca table.

    This table exists to please macOS. macOS considers a font valid if it has this table.
    """

    def __init__(self):

        self.tableName = "loca" # hard-coded. For font generation only.
        self.whatever = 0

        # This table's type is determined by head.indexToLocFormat.
        # TODO: make a version of loca that can be used in bytes compilation.

    def toTTX(self):
        return Element("loca")

    def toBytes(self):
        return padTableBytes(b'\0') # TODO: make a bytes representation

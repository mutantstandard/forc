from lxml.etree import Element


class loca:
    """
    Class representing a placeholder loca table.

    This table exists to please macOS. macOS considers a font valid if it has this table.
    """

    def __init__(self):
        self.whatever = 0

        # This table's type is determined by head.indexToLocFormat.

    def toTTX(self):
        return Element("loca")

import struct

from lxml.etree import Element
from tables.support.ebxBitmaps import EBDTBitmapFormat17


class CBDTStrike:
    """
    A class representing a CBDT strike in a CBDT strike.
    """

    def __init__(self, glyphs, metrics, strikeRes):
        self.glyphs = []

        for g in glyphs["img"]: #img is used here because CBDT bitmaps are identified by glyph name.
            self.glyphs.append(EBDTBitmapFormat17(metrics, strikeRes, g))


    def toTTX(self, index):
        strikedata = Element("strikedata", {"index": str(index)})


        for g in self.glyphs:
            strikedata.append(g.toTTX())

        return strikedata


class CBDT:
    """
    A class representing a CBDT table.
    """

    def __init__(self, m, glyphs):

        self.tableName = "CBDT" # hard-coded.  For font generation only.

        self.majorVersion = 3
        self.minorVersion = 0
        # hard-coded. the only version available right now.
        # presumably needs to agree with CBLC's version.


        self.strikes = []


        # iterate over each strike.
        strikeIndex = 0

        for imageFormat, image in glyphs["img"][0].imgDict.items():
            if imageFormat.split('-')[0] == "png":
                strikeRes = imageFormat.split('-')[1]
                self.strikes.append(CBDTStrike(glyphs, m["metrics"], strikeRes))

                strikeIndex += 1


    def toTTX(self):
        cbdt = Element("CBDT")
        cbdt.append(Element("header", {"version": f"{self.majorVersion}.{self.minorVersion}"}))

        strikeIndex = 0
        for strike in self.strikes:
            cbdt.append(strike.toTTX(strikeIndex))
            strikeIndex += 1

        return cbdt

    def toBytes(self):
        cbdt = struct.pack( ">HH"
                          , self.majorVersion # UInt16
                          , self.minorVersion # UInt16
                          )
        return cbdt # placeholder
        # TODO: pack all of the image data immediately after~

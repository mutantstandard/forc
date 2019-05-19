from lxml.etree import Element
from tables.support.EBxBitmaps import EBDTBitmapFormat17


class cbdtStrike:
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


class cbdt:
    """
    A class representing a CBDT table.
    """

    def __init__(self, m, glyphs):
        self.headerVersion = 3.0 # hard-coded. the only version available right now.
        self.strikes = []


        # get basic strike information by poking for a glyph
        # that has strikes.

        for g in glyphs["img_empty"]:
            if g.imgDict:
                firstGlyphWithStrikes = g
                break

        # iterate over each strike.
        strikeIndex = 0

        for imageFormat, image in firstGlyphWithStrikes.imgDict.items():
            if imageFormat.split('-')[0] == "png":
                strikeRes = imageFormat.split('-')[1]
                self.strikes.append(cbdtStrike(glyphs, m["metrics"], strikeRes))

                strikeIndex += 1


    def toTTX(self):
        cbdt = Element("CBDT")
        cbdt.append(Element("header", {"version": str(self.headerVersion)})) # hard-coded

        strikeIndex = 0
        for strike in self.strikes:
            cbdt.append(strike.toTTX(strikeIndex))
            strikeIndex += 1

        return cbdt

from lxml.etree import Element
from tables.support.ebx_metrics import BitmapSize
from tables.support.ebx_indexes import IndexSubTable1



class cblcStrike:

    def __init__(self, metrics, index, ppem, glyphs):

        self.index = index
        self.bitmapSizeTable = BitmapSize(metrics, ppem, glyphs)
        self.indexSubTable = IndexSubTable1(glyphs)


    def toTTX(self):
        strike = Element("strike", {"index": str(self.index) })

        strike.append(self.bitmapSizeTable.toTTX())
        strike.append(self.indexSubTable.toTTX())

        return strike



class cblc:

    def __init__(self, m, glyphs):

        self.version = float(3.0) # hard-coded, the only CBLC version that exists.
        self.strikes = []

        # get basic strike information.

        for g in glyphs["img_empty"]:
            if g.imgDict:
                firstGlyphWithStrikes = g
                break

        # iterate over each strike.
        strikeIndex = 0

        for imageFormat, image in firstGlyphWithStrikes.imgDict.items():
            if imageFormat.split('-')[0] == "png":
                self.strikes.append(cblcStrike(m["metrics"], strikeIndex, image.strike, glyphs))
                strikeIndex += 1


    def toTTX(self):
        cblc = Element("CBLC")
        cblc.append(Element("header", {"version": str(self.version) })) # hard-coded

        for s in self.strikes:
            cblc.append(s.toTTX())

        return cblc

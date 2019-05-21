from lxml.etree import Element
from tables.support.ebxMetrics import BitmapSize
from tables.support.ebxIndexes import IndexSubTable1



class cblcStrike:

    def __init__(self, metrics, ppem, glyphs):

        self.bitmapSizeTable = BitmapSize(metrics, ppem, glyphs)
        self.indexSubTable = IndexSubTable1(glyphs)


    def toTTX(self, index):
        strike = Element("strike", {"index": str(index) })

        strike.append(self.bitmapSizeTable.toTTX())
        strike.append(self.indexSubTable.toTTX())

        return strike



class cblc:

    def __init__(self, m, glyphs):

        self.version = float(3.0) # hard-coded, the only CBLC version that exists.
        self.strikes = []

        # iterate over each strike.


        for imageFormat, image in glyphs["img"][0].imgDict.items():
            if imageFormat.split('-')[0] == "png":
                self.strikes.append(cblcStrike(m["metrics"], image.strike, glyphs))



    def toTTX(self):
        cblc = Element("CBLC")
        cblc.append(Element("header", {"version": str(self.version) })) # hard-coded

        strikeIndex = 0

        for s in self.strikes:
            cblc.append(s.toTTX(strikeIndex))
            strikeIndex += 1

        return cblc

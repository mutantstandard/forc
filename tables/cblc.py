import struct
from lxml.etree import Element
from tables.support.ebxMetrics import SbitLineMetrics
from tables.support.ebxIndexes import IndexSubTable1


class CBLCBitmapSize:
    """
    A class representation of an CBLC BitmapSize subtable.

    This is similar to, but not the same as, an EBLC BitmapSize subtable.
    """

    def __init__(self, metrics, ppem, glyphs):

        self.indexSubTables = []
        self.indexSubTables.append(IndexSubTable1(glyphs))

        self.colorRef = 0 # TODO: ???
        self.hori = SbitLineMetrics('hori', metrics)
        self.vert = SbitLineMetrics('vert', metrics)
        self.ppemX = ppem
        self.ppemY = ppem
        self.bitDepth = 32 # 32 is the bitdepth for colour emoji. hard-coded for now.
        self.flags = 1 # TODO: figure out how this actually works.

        glyphIDList = []
        for id, g in enumerate(glyphs['img_empty']):
            if g.imgDict:
                glyphIDList.append(id)

        self.startGlyphIndex = glyphIDList[0]
        self.endGlyphIndex = glyphIDList[-1]




    def toTTX(self, index):
        """
        Returns a TTX version of this table element.

        TTX structures BitmapSize tables differently to a normal binary font -
        BitmapSizes and IndexSubtables that correspond to the same strike are
        bundled together as a '<strike>'.)
        """

        strike = Element("strike", {"index": str(index) })

        bSizeTable = Element("bitmapSizeTable")

        bSizeTable.append(self.hori.toTTX())
        bSizeTable.append(self.vert.toTTX())

        bSizeTable.append(Element("colorRef", {"value": str(self.colorRef) }))

        bSizeTable.append(Element("startGlyphIndex", {"value": str(self.startGlyphIndex) }))
        bSizeTable.append(Element("endGlyphIndex", {"value": str(self.endGlyphIndex) }))

        bSizeTable.append(Element("ppemX", {"value": str(self.ppemX) }))
        bSizeTable.append(Element("ppemY", {"value": str(self.ppemY) }))

        bSizeTable.append(Element("bitDepth", {"value": str(self.bitDepth) }))
        bSizeTable.append(Element("flags", {"value": str(self.flags) }))

        strike.append(bSizeTable)

        for s in self.indexSubTables:
            strike.append(s.toTTX())

        return strike



    def toBytes(self):
        """
        Returns a bytes version of this table element.

        Fonts structure BitmapSize differently to TTX. Each chunk of
        data is laid out linearly:

        - Array of all BitmapSizes (containing offsets to attached IndexSubTable(s))
        - Array of all IndexSubTables

        TODO: figure out how to do this.
        """




class CBLC:

    def __init__(self, m, glyphs):

        self.majorVersion = 3
        self.minorVersion = 0
        # hardcoded; the only CBLC version that exists.

        self.bitmapSizeTables = []

        # iterate over each strike.


        for imageFormat, image in glyphs["img"][0].imgDict.items():
            if imageFormat.split('-')[0] == "png":
                self.bitmapSizeTables.append(CBLCBitmapSize(m["metrics"], image.strike, glyphs))



    def toTTX(self):
        cblc = Element("CBLC")
        cblc.append(Element("header", {"version": f"{self.majorVersion}.{self.minorVersion}" }))

        strikeIndex = 0

        for s in self.bitmapSizeTables:
            cblc.append(s.toTTX(strikeIndex))
            strikeIndex += 1

        return cblc

    def toBytes(self):
        return struct.pack( ">HHI"
                          , self.majorVersion # UInt16
                          , self.minorVersion  # UInt16
                          , len(self.bitmapSizeTables) # UInt32 (numSizes)
                          # pack all of the BitmapSize tables immediately after.
                          )

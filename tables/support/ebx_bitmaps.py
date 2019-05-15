from lxml.etree import Element
from tables.support.ebx_metrics import SmallGlyphMetrics, BigGlyphMetrics



class EBDTBitmapFormat17:
    """
    Class representing a CBDT format 17 bitmap subtable.

    (this is the only CBDT subtable format supported by TTX)
    """
    def __init__(self, metrics, strikeRes, glyph):
        self.name = glyph.codepoints.name()
        self.metrics = SmallGlyphMetrics(metrics)
        self.img = glyph.imgDict["png-" + strikeRes]


    def toTTX(self):
        # format 18 for big metrics and PNG data.
        bitmapTable = Element("cbdt_bitmap_format_17", {"name": self.name })

        bitmapTable.append(self.metrics.toTTX())

        rawImageData = Element("rawimagedata")
        rawImageData.text = self.img.getHexDump()
        bitmapTable.append(rawImageData)

        return bitmapTable




class EBDTBitmapFormat18:
    """
    Class representing a CBDT format 17 bitmap subtable.

    (This is not supported by TTX)
    """

    def __init__(self, metrics, strikeRes, img):
        self.name = glyph.codepoints.name()
        self.metrics = BigGlyphMetrics(metrics)
        self.img = img


    def toTTX(self):
        # format 18 for big metrics and PNG data.
        bitmapTable = Element("cbdt_bitmap_format_18", {"name": self.name })

        bitmapTable.append(self.metrics.toTTX())

        rawImageData = Element("rawimagedata")
        rawImageData.text = self.img.getHexDump()
        bitmapTable.append(rawImageData)

        return bitmapTable



class EBDTBitmapFormat19:
    """
    Class representing a CBDT format 19 bitmap subtable.

    (This is not supported by TTX)
    """

    def __init__(self, metrics, strikeRes, img):
        self.name = glyph.codepoints.name()
        self.img = img


    def toTTX(self):
        # format 18 for big metrics and PNG data.
        bitmapTable = Element("cbdt_bitmap_format_19", {"name": self.name })

        rawImageData = Element("rawimagedata")
        rawImageData.text = self.img.getHexDump()
        bitmapTable.append(rawImageData)

        return bitmapTable

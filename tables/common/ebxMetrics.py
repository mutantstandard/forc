
import struct

from lxml.etree import Element






bitScale = 127

def getLocalScale(metrics):
    return max(metrics['height'], metrics['width'])



class SmallGlyphMetrics:
    """
    A class representation of a EBDT/EBLC/CBDT/CBLC SmallGlyphMetrics subtable.
    """

    def __init__(self, metrics):

        localScale = getLocalScale(metrics)

        self.height =      round( (metrics['height'] / localScale) * bitScale )
        self.width =       round( (metrics['width'] / localScale) * bitScale )

        self.bearingX =    round( (metrics['xMin'] / localScale) * bitScale )
        self.bearingY =    bitScale+(round( (metrics['yMin'] / localScale) * bitScale ))
        self.advance =     self.width


    def toTTX(self):
        glyphMetrics = Element("SmallGlyphMetrics")
        glyphMetrics.append(Element("height",          {"value": str(self.height) }))
        glyphMetrics.append(Element("width",           {"value": str(self.width) }))
        glyphMetrics.append(Element("BearingX",    {"value": str(self.bearingX) }))
        glyphMetrics.append(Element("BearingY",    {"value": str(self.bearingY) }))
        glyphMetrics.append(Element("Advance",     {"value": str(self.advance) }))

        return glyphMetrics


    def toBytes(self):
        return struct.pack('>BBbbB'
                          , self.height # UInt8
                          , self.width # UInt8
                          , self.bearingX # Int8
                          , self.bearingY # Int8
                          , self.advance # UInt8
                          )


class BigGlyphMetrics:
    """
    A class representation of a EBDT/EBLC/CBDT/CBLC BigGlyphMetrics subtable.
    """

    def __init__(self, metrics):
        localScale = getLocalScale(metrics)

        self.height =          round( (metrics['height'] / localScale) * bitScale )
        self.width =           round( (metrics['width'] / localScale) * bitScale )

        self.horiBearingX =    round( (metrics['xMin'] / localScale) * bitScale )
        self.horiBearingY =    bitScale+(round( (metrics['yMin'] / localScale) * bitScale ))
        self.horiAdvance =     self.width

        self.vertBearingX =    round( (metrics['xMin'] / localScale) * bitScale )
        self.vertBearingY =    round( (metrics['yMin'] / localScale) * bitScale )
        self.vertAdvance =     self.height


    def toTTX(self):
        glyphMetrics = Element("BigGlyphMetrics")
        glyphMetrics.append(Element("height",          {"value": str(self.height) }))
        glyphMetrics.append(Element("width",           {"value": str(self.width) }))
        glyphMetrics.append(Element("horiBearingX",    {"value": str(self.horiBearingX) }))
        glyphMetrics.append(Element("horiBearingY",    {"value": str(self.horiBearingY) }))
        glyphMetrics.append(Element("horiAdvance",     {"value": str(self.horiAdvance) }))
        glyphMetrics.append(Element("vertBearingX",    {"value": str(self.vertBearingX) }))
        glyphMetrics.append(Element("vertBearingY",    {"value": str(self.vertBearingY) }))
        glyphMetrics.append(Element("vertAdvance",     {"value": str(self.vertAdvance) }))

        return glyphMetrics


    def toBytes(self):
        return struct.pack('>BBbbBbbB'
                          , self.height # UInt8
                          , self.width # UInt8
                          , self.horiBearingX # Int8
                          , self.horiBearingY # Int8
                          , self.horiAdvance # UInt8
                          , self.vertBearingX # Int8
                          , self.vertBearingY # Int8
                          , self.vertAdvance # UInt8
                          )


class SbitLineMetrics:
    """
    Creates a TTX representation of a EBDT/EBLC/CBDT/CBLC sbitLineMetrics subtable.
    """

    def __init__(self, direction, metrics):

        self.direction = direction

        localScale = getLocalScale(metrics)

        if direction is 'hori':
            self.ascender =  round( (metrics['yMax'] / localScale) * bitScale )
            self.descender = round( (metrics['yMin'] / localScale) * bitScale )
            self.widthMax =  round( (metrics['width'] / localScale) * bitScale )

        elif direction is 'vert':
            self.ascender =  round( (metrics['yMax'] / localScale) * bitScale )
            self.descender = round( (metrics['yMin'] / localScale) * bitScale )
            self.widthMax =  round( (metrics['width'] / localScale) * bitScale )

        self.caretSlopeNumerator = 0 # hard coded because emoji
        self.caretSlopeDenominator = 0 # hard coded because emoji
        self.caretOffset = 0 # hard coded because emoji

        self.minOriginSB = 0
        self.minAdvanceSB = 0
        self.maxBeforeBL = 0
        self.minAfterBL = 0
        self.pad1 = 0
        self.pad2 = 0


    def toTTX(self):
        metrics = Element("sbitLineMetrics", {"direction": self.direction})

        metrics.append(Element("ascender", {"value": str(self.ascender) }))
        metrics.append(Element("descender", {"value": str(self.descender) }))
        metrics.append(Element("widthMax", {"value": str(self.widthMax) }))

        metrics.append(Element("caretSlopeNumerator", {"value": str(self.caretSlopeNumerator) }))
        metrics.append(Element("caretSlopeDenominator", {"value": str(self.caretSlopeDenominator) }))
        metrics.append(Element("caretOffset", {"value": str(self.caretOffset) }))

        metrics.append(Element("minOriginSB", {"value": str(self.minOriginSB) }))
        metrics.append(Element("minAdvanceSB", {"value": str(self.minAdvanceSB) }))

        metrics.append(Element("maxBeforeBL", {"value": str(self.maxBeforeBL) }))
        metrics.append(Element("minAfterBL", {"value": str(self.minAfterBL) }))
        metrics.append(Element("pad1", {"value": str(self.pad1) }))
        metrics.append(Element("pad2", {"value": str(self.pad2) }))

        return metrics


    def toBytes(self):
        return struct.pack('>bbBbbbbbbbbb'
                          , self.ascender # Int8
                          , self.descender # Int8
                          , self.widthMax # UInt8

                          , self.caretSlopeNumerator # Int8
                          , self.caretSlopeDenominator # Int8
                          , self.caretOffset # Int8

                          , self.minOriginSB # Int8
                          , self.minAdvanceSB # Int8
                          , self.maxBeforeBL # Int8
                          , self.minAfterBL # Int8
                          , self.pad1 # Int8
                          , self.pad1 # Int8
                          )

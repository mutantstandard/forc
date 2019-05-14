from lxml.etree import Element

bitScale = 127




def getLocalScale(metrics):
    return max(metrics['height'], metrics['width'])



class SmallGlyphMetrics:
    """
    A representation of a EBDT/EBLC/CBDT/CBLC SmallGlyphMetrics subtable.
    """

    def __init__(self, metrics):

        localScale = getLocalScale(metrics)

        self.height =      round( (metrics['height'] / localScale) * bitScale )
        self.width =       round( (metrics['width'] / localScale) * bitScale )

        self.BearingX =    round( (metrics['xMin'] / localScale) * bitScale )
        self.BearingY =    bitScale+(round( (metrics['yMin'] / localScale) * bitScale ))
        self.Advance =     self.width


    def toTTX(self):
        glyphMetrics = Element("SmallGlyphMetrics")
        glyphMetrics.append(Element("height",          {"value": str(self.height) }))
        glyphMetrics.append(Element("width",           {"value": str(self.width) }))
        glyphMetrics.append(Element("BearingX",    {"value": str(self.BearingX) }))
        glyphMetrics.append(Element("BearingY",    {"value": str(self.BearingY) }))
        glyphMetrics.append(Element("Advance",     {"value": str(self.Advance) }))

        return glyphMetrics




class BigGlyphMetrics:
    """
    Creates a TTX representation of a EBDT/EBLC/CBDT/CBLC BigGlyphMetrics subtable.
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




def sbitLineMetricsHori(metrics):
    """
    Creates a TTX representation of a EBDT/EBLC/CBDT/CBLC sbitLineMetrics (horizontal) subtable.
    """

    localScale = getLocalScale(metrics)

    horiAscender =  round( (metrics['yMax'] / localScale) * bitScale )
    horiDescender = round( (metrics['yMin'] / localScale) * bitScale )
    horiWidthMax =  round( (metrics['width'] / localScale) * bitScale )

    metrics = Element("sbitLineMetrics", {"direction": "hori"})

    metrics.append(Element("ascender", {"value": str(horiAscender) }))
    metrics.append(Element("descender", {"value": str(horiDescender) }))
    metrics.append(Element("widthMax", {"value": str(horiWidthMax) }))

    metrics.append(Element("caretSlopeNumerator", {"value": "0"}))    # hard-coded
    metrics.append(Element("caretSlopeDenominator", {"value": "0"}))  # hard-coded
    metrics.append(Element("caretOffset", {"value": "0"}))            # hard-coded

    metrics.append(Element("minOriginSB", {"value": "0"}))
    metrics.append(Element("minAdvanceSB", {"value": "0" }))

    metrics.append(Element("maxBeforeBL", {"value": "0"}))
    metrics.append(Element("minAfterBL", {"value": "0" }))
    metrics.append(Element("pad1", {"value": "0"}))
    metrics.append(Element("pad2", {"value": "0"}))

    return metrics


def sbitLineMetricsVert(metrics):
    """
    Creates a TTX representation of a EBDT/EBLC/CBDT/CBLC sbitLineMetrics (vertical) subtable.

    I'm pretty confident this isn't proper, but vertical metrics
    aren't actually properly represented in this font builder at present.
    """

    localScale = getLocalScale(metrics)

    vertAscender =  round( (metrics['yMax'] / localScale) * bitScale )
    vertDescender = round( (metrics['yMin'] / localScale) * bitScale )
    vertWidthMax =  round( (metrics['width'] / localScale) * bitScale )

    metrics = Element("sbitLineMetrics", {"direction": "vert"})

    metrics.append(Element("ascender", {"value": str(vertAscender) }))
    metrics.append(Element("descender", {"value": str(vertDescender) }))
    metrics.append(Element("widthMax", {"value": str(vertWidthMax) }))

    metrics.append(Element("caretSlopeNumerator", {"value": "0"}))      # hard-coded
    metrics.append(Element("caretSlopeDenominator", {"value": "0"}))    # hard-coded
    metrics.append(Element("caretOffset", {"value": "0"}))              # hard-coded

    metrics.append(Element("minOriginSB", {"value": "0"}))
    metrics.append(Element("minAdvanceSB", {"value": "0" }))

    metrics.append(Element("maxBeforeBL", {"value": "0"}))
    metrics.append(Element("minAfterBL", {"value": "0" }))
    metrics.append(Element("pad1", {"value": "0"}))
    metrics.append(Element("pad2", {"value": "0"}))

    return metrics

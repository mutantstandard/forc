from lxml.etree import Element

bitScale = 127




def getLocalScale(metrics):
    return max(metrics['height'], metrics['width'])



def SmallGlyphMetrics(metrics):
    """
    Creates a TTX representation of a EBDT/EBLC/CBDT/CBLC SmallGlyphMetrics subtable.
    """

    localScale = getLocalScale(metrics)

    height =      round( (metrics['height'] / localScale) * bitScale )
    width =       round( (metrics['width'] / localScale) * bitScale )

    BearingX =    round( (metrics['xMin'] / localScale) * bitScale )
    BearingY =    bitScale+(round( (metrics['yMin'] / localScale) * bitScale ))
    Advance =     width



    glyphMetrics = Element("SmallGlyphMetrics")
    glyphMetrics.append(Element("height",          {"value": str(height) }))
    glyphMetrics.append(Element("width",           {"value": str(width) }))
    glyphMetrics.append(Element("BearingX",    {"value": str(BearingX) }))
    glyphMetrics.append(Element("BearingY",    {"value": str(BearingY) }))
    glyphMetrics.append(Element("Advance",     {"value": str(Advance) }))

    return glyphMetrics




def BigGlyphMetrics(metrics):
    """
    Creates a TTX representation of a EBDT/EBLC/CBDT/CBLC BigGlyphMetrics subtable.
    """

    localScale = getLocalScale(metrics)

    height =          round( (metrics['height'] / localScale) * bitScale )
    width =           round( (metrics['width'] / localScale) * bitScale )

    horiBearingX =    round( (metrics['xMin'] / localScale) * bitScale )
    horiBearingY =    bitScale+(round( (metrics['yMin'] / localScale) * bitScale ))
    horiAdvance =     width

    vertBearingX =    round( (metrics['xMin'] / localScale) * bitScale )
    vertBearingY =    round( (metrics['yMin'] / localScale) * bitScale )
    vertAdvance =     height


    glyphMetrics = Element("BigGlyphMetrics")
    glyphMetrics.append(Element("height",          {"value": str(height) }))
    glyphMetrics.append(Element("width",           {"value": str(width) }))
    glyphMetrics.append(Element("horiBearingX",    {"value": str(horiBearingX) }))
    glyphMetrics.append(Element("horiBearingY",    {"value": str(horiBearingY) }))
    glyphMetrics.append(Element("horiAdvance",     {"value": str(horiAdvance) }))
    glyphMetrics.append(Element("vertBearingX",    {"value": str(vertBearingX) }))
    glyphMetrics.append(Element("vertBearingY",    {"value": str(vertBearingY) }))
    glyphMetrics.append(Element("vertAdvance",     {"value": str(vertAdvance) }))

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

from lxml.etree import Element


def SmallGlyphMetrics(metrics):
    """
    Creates a TTX representation of a EBDT/EBLC/CBDT/CBLC SmallGlyphMetrics subtable.
    """

    height =      round( (metrics['height'] / metrics['height']) * 128 )
    width =       round( (metrics['width'] / metrics['height']) * 128 )

    BearingX =    round( (metrics['xMin'] / metrics['height']) * 128 )
    BearingY =    128+(round( (metrics['yMin'] / metrics['height']) * 128 ))
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

    height =          round( (metrics['height'] / metrics['height']) * 128 )
    width =           round( (metrics['width'] / metrics['height']) * 128 )

    horiBearingX =    round( (metrics['xMin'] / metrics['height']) * 128 )
    horiBearingY =    round( (metrics['yMin'] / metrics['height']) * 128 )
    horiAdvance =     width

    vertBearingX =    round( (metrics['xMin'] / metrics['height']) * 128 )
    vertBearingY =    round( (metrics['yMin'] / metrics['height']) * 128 )
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

    horiAscender =  round( (metrics['yMax'] / metrics['height']) * 128 )
    horiDescender = round( (metrics['yMin'] / metrics['height']) * 128 )
    horiWidthMax =  round( (metrics['width'] / metrics['height']) * 128 )

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

    vertAscender =  round( (metrics['yMax'] / metrics['height']) * 128 )
    vertDescender = round( (metrics['yMin'] / metrics['height']) * 128 )
    vertWidthMax =  round( (metrics['width'] / metrics['height']) * 128 )

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

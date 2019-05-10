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

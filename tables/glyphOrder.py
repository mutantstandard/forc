from xml.etree.ElementTree import Element

def glyphOrder():
    """
    Generates and returns a GlyphOrder XML element.

    GlyphOrder is not a table, but sort of a helper for TTX.
    This does not appear in the tables of a finished font.
    """
    glyphOrder = Element("GlyphOrder")

    # here you will need to add all of the juicy glyphs.

    return glyphOrder

from lxml.etree import Element

def create(glyphs):
    """
    Generates and returns a GlyphOrder XML element.

    GlyphOrder is not a table, but sort of a helper for TTX.
    This does not appear in the tables of a finished font.
    """


    glyphOrder = Element("GlyphOrder")

    # add all of the juicy glyphs
    for id, g in enumerate(glyphs['img']):
        glyphOrder.append(Element("GlyphID", {"id": str(id), "name": g.codepoints.name() }))


    return glyphOrder

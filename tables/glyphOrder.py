from lxml.etree import Element

class GlyphOrder:
    """
    Class representing a GlyphOrder table.

    GlyphOrder is not a table (I think???), but sort of a helper for TTX.
    This does not appear in the tables of a finished font.
    """

    def __init__(self, glyphs):
        self.glyphs = {}

        for id, g in enumerate(glyphs["img_empty"]):
            self.glyphs[id] = g


    def toTTX(self):
        glyphOrder = Element("GlyphOrder")

        for id, g in self.glyphs.items():
            glyphOrder.append(Element("GlyphID", {"id": str(id), "name": g.name() }))


        return glyphOrder

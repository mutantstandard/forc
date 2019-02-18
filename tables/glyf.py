from lxml.etree import Element, ElementTree

def glyf(glyphs):
    """
    Generates and returns a glyf table with dummy data.
    """

    glyfTable = Element("glyf")



    for ID, g in enumerate(glyphs):
            glyfTable.append(Element("TTGlyph", {"name": g.name}))


    return glyfTable

from lxml.etree import Element, ElementTree

def glyf(glyphs):
    """
    Generates and returns a glyf table with dummy data.
    """

    glyfTable = Element("glyf")



    for ID, g in enumerate(glyphs):

        if ID is 0:
            # make a dummy contour for .notdef.
            # for some reason (according to macOS validation) it's important.
            # the others can be blank

            dummyDataNotDef = Element("TTGlyph",    {"name": g.name
                                                    ,"xMin": "0"
                                                    ,"xMax": "0"
                                                    ,"yMin": "0"
                                                    ,"yMax": "0"
                                                    })
            dummyContours = Element("contour")
            dummyContours.append(Element("pt", {"x": "100", "y": "100", "on": "1"}))

            dummyDataNotDef.append(dummyContours)
            dummyDataNotDef.append(Element("instructions"))

            glyfTable.append(dummyDataNotDef)

        else:
            # make the others blank because nothing is depending on
            # them actually having glyf contours and we don't want them.

            glyfTable.append(Element("TTGlyph", {"name": g.name}))


    return glyfTable

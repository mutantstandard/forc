from lxml.etree import Element, ElementTree

def create(m, glyphs):
    """
    Generates and returns a glyf table with dummy data.
    """

    metrics = m["metrics"]

    glyfTable = Element("glyf")

    fakeGlyfs = 0

    for ID, g in enumerate(glyphs["img_empty"]):


        # create one dummy glyf in the right place
        if g.codepoints.seq[0] not in [int('0x0020', 16), int('0x200d', 16), int('0xfe0f', 16)]:

            # make a dummy contour for .notdef.
            # for some reason (according to macOS validation) it's important.
            # the others can be blank

            # These attributes will be calculated by the compiler.
            dummyDataNotDef = Element("TTGlyph",    {"name": g.codepoints.name()
                                                    ,"xMin": str(metrics["xMin"])
                                                    ,"xMax": str(metrics["xMax"])
                                                    ,"yMin": str(metrics["yMin"])
                                                    ,"yMax": str(metrics["yMax"])
                                                    })


            # these dummy contours are designed to trick the TTX compiler to making sure the
            # xMin/yMin/etc. parameters of the font are set to what we want them to actually be set to.
            # (TTX will ignore the user's parameters if what's in the glyf table doesn't agree.)

            dummyContour1 = Element("contour")
            dummyContour1.append(Element("pt", {"x": str(metrics["xMin"]), "y": str(metrics["yMin"]), "on": "1"}))

            dummyDataNotDef.append(dummyContour1)


            dummyContour2 = Element("contour")

            dummyDataNotDef.append(dummyContour2)


            dummyDataNotDef.append(Element("instructions"))
            dummyContour2.append(Element("pt", {"x": str(metrics["xMax"]), "y": str(metrics["yMax"]), "on": "1"}))
            glyfTable.append(dummyDataNotDef)

            fakeGlyfs += 1


        else:
            # make the others blank because nothing is depending on
            # them actually having glyf contours and we don't want them.

            glyfTable.append(Element("TTGlyph", {"name": g.codepoints.name() }))


    return glyfTable

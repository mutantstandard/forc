from lxml.etree import Element, ElementTree

def glyf(m, glyphs):
    """
    Generates and returns a glyf table with dummy data.
    """

    glyfTable = Element("glyf")

    fakeGlyfs = 0

    for ID, g in enumerate(glyphs['img']):


        # create one dummy glyf in the right place
        if g.codepoints[0] not in [int('0x0020', 16), int('0x200d', 16), int('0xfe0f', 16)]:

            if fakeGlyfs < 1:

                # make a dummy contour for .notdef.
                # for some reason (according to macOS validation) it's important.
                # the others can be blank

                # These attributes will be calculated by the compiler.
                dummyDataNotDef = Element("TTGlyph",    {"name": g.name
                                                        ,"xMin": "0"
                                                        ,"xMax": "0"
                                                        ,"yMin": "0"
                                                        ,"yMax": "0"
                                                        })
                dummyContours = Element("contour")


                # these dummy contours are designed to trick the TTX compiler to making sure the
                # xMin/yMin/etc. parameters of the font are set to what we want them to actually be set to.
                # (TTX will ignore the user's parameters if what's in the glyf table doesn't agree.)

                dummyContours.append(Element("pt", {"x": str(m["metrics"]["xMax"]), "y": str(m["metrics"]["yMax"]), "on": "1"}))
                dummyContours.append(Element("pt", {"x": str(m["metrics"]["xMin"]), "y": str(m["metrics"]["yMin"]), "on": "1"}))

                dummyDataNotDef.append(dummyContours)
                dummyDataNotDef.append(Element("instructions"))

                glyfTable.append(dummyDataNotDef)

                fakeGlyfs += 1

            else:
                glyfTable.append(Element("TTGlyph", {"name": g.name}))

        else:
            # make the others blank because nothing is depending on
            # them actually having glyf contours and we don't want them.

            glyfTable.append(Element("TTGlyph", {"name": g.name}))


    return glyfTable

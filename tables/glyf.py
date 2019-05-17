from lxml.etree import Element, ElementTree

def toTTX(m, glyphs):
    """
    Generates and returns a glyf table with dummy data.
    """

    metrics = m["metrics"]

    glyfTable = Element("glyf")

    for ID, g in enumerate(glyphs["img_empty"]):

        # if it's not a whitespace character or a service glyph....
        if g.type is "empty":
            glyfTable.append(Element("TTGlyph", {"name": g.name() }))

        # if it's not one of these, it needs some dummy glyf contours

        else:
            # These attributes will be calculated by the TTX compiler,
            # but I'm doing them manually anyway.
            dummyData = Element("TTGlyph",    {"name": g.name()
                                                    ,"xMin": str(metrics["xMin"])
                                                    ,"xMax": str(metrics["xMax"])
                                                    ,"yMin": str(metrics["yMin"])
                                                    ,"yMax": str(metrics["yMax"])
                                                    })


            # these dummy contours are designed to establish a bounding box to trick
            # the TTX compiler to making sure the head.xMin/head.yMin/etc. parameters
            # of the font are set to what we want them to actually be set to.
            #
            # (This is because TTX will overwrite the user's head.xMin etc. parameters
            # if what's in the glyf table doesn't agree.)

            dummyContour1 = Element("contour")
            dummyContour1.append(Element("pt", {"x": str(metrics["xMin"]), "y": str(metrics["yMin"]), "on": "1"}))
            dummyData.append(dummyContour1)

            dummyContour2 = Element("contour")
            dummyContour2.append(Element("pt", {"x": str(metrics["xMax"]), "y": str(metrics["yMax"]), "on": "1"}))
            dummyData.append(dummyContour2)

             # this is important, even though I don't know what it's for
            dummyData.append(Element("instructions"))

            glyfTable.append(dummyData)



    return glyfTable

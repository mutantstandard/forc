from lxml.etree import Element, ElementTree


class glyf:
    """
    Class representing a glyf table.
    (this currently doesn't accurately represent a glyf table in bytes)
    """

    def __init__(self, m, glyphs):

        self.tableName = "glyf" # hard-coded.  For font generation only.
        
        self.glyphs = []
        self.xMin = m['metrics']['xMin']
        self.yMin = m['metrics']['yMin']
        self.xMax = m['metrics']['xMax']
        self.yMax = m['metrics']['yMax']

        for g in glyphs["img_empty"]:
            self.glyphs.append(g)


    def toTTX(self):
        glyf = Element("glyf")

        for g in self.glyphs:

            # if it's not a whitespace character or a service glyph....
            if g.glyphType is "empty":
                glyf.append(Element("TTGlyph", {"name": g.name() }))


            # if it's not one of these, it needs some dummy glyf contours
            else:
                # These attributes will be calculated by the TTX compiler,
                # but I'm doing them manually anyway.
                dummyData = Element("TTGlyph",    {"name": g.name()
                                                        ,"xMin": str(self.xMin)
                                                        ,"xMax": str(self.xMax)
                                                        ,"yMin": str(self.yMin)
                                                        ,"yMax": str(self.yMax)
                                                        })


                # these dummy contours are designed to establish a bounding box to trick
                # the TTX compiler to making sure the head.xMin/head.yMin/etc. parameters
                # of the font are set to what we want them to actually be set to.
                #
                # (This is because TTX will overwrite the user's head.xMin etc. parameters
                # if what's in the glyf table doesn't agree.)

                dummyContour1 = Element("contour")
                dummyContour1.append(Element("pt", {"x": str(self.xMin), "y": str(self.yMin), "on": "1"}))
                dummyData.append(dummyContour1)

                dummyContour2 = Element("contour")
                dummyContour2.append(Element("pt", {"x": str(self.xMax), "y": str(self.yMax), "on": "1"}))
                dummyData.append(dummyContour2)

                 # this is important, even though I don't know what it's for
                dummyData.append(Element("instructions"))

                glyf.append(dummyData)

        return glyf

    # TODO: learn how to convert glyf to bytes.

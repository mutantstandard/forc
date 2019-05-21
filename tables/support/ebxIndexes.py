from lxml.etree import Element

# For storing EBLC/CBLC/bloc IndexSubTable classes.
# (bloc only supports table formats 1-3.)


class IndexSubTable1:
    """
    Class representing an EBLC/CBLC/bloc IndexSubTable, format 1.
    """
    def __init__(self, glyphs):
        self.glyphs = []

        for id, g in enumerate(glyphs["img_empty"]):
            if g.imgDict:
                self.glyphs.append({"id": id, "name": g.name() })


    def toTTX(self):
        eblcSub = Element("eblc_index_sub_table_1", { "imageFormat": "17" #TODO: Do something about image format nums.
                                                    , "firstGlyphIndex": str(self.glyphs[0]["id"])
                                                    , "lastGlyphIndex": str(self.glyphs[-1]["id"])
                                                    })

        for g in self.glyphs:
            eblcSub.append(Element("glyphLoc", {"id": str(g["id"]), "name": g["name"] }))

        return eblcSub

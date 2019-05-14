from lxml.etree import Element


class sbixBitmap:
    """
    Class representing a single bitmap within a strike within an sbix table.
    """
    def __init__(self, glyph, ppem):
        self.name = glyph.codepoints.name()
        self.graphicType = "png " # hard-coded for now
        self.originOffsetX = 0 # hard-coded for now
        self.originOffsetY = 0 # hard-coded for now

        # forc img class or None
        if glyph.img:
            self.img = glyph.img["png-" + str(ppem)]
        else:
            self.img = None


    def toTTX(self):
        if not self.img:
            return Element("glyph", {"name": self.name })
        else:
            sbixBitmap = Element("glyph",   {"name": self.name
                                            ,"graphicType": self.graphicType
                                            ,"originOffsetX": str(self.originOffsetX)
                                            ,"originOffsetY": str(self.originOffsetY)
                                            })
            hexdata = Element("hexdata")
            hexdata.text = self.img.getHexDump()

            sbixBitmap.append(hexdata)

            return sbixBitmap




class sbixStrike:
    """
    Class representing a single strike within an sbix table.
    """
    def __init__(self, ppem, glyphs):
        self.ppem = ppem
        self.ppi = 72 # hard-coded for now

        self.bitmaps = []

        for g in glyphs:
            self.bitmaps.append( sbixBitmap(g, ppem) )


    def toTTX(self):
        strike = Element("strike")
        strike.append(Element("ppem", {"value": str(self.ppem) }))
        strike.append(Element("resolution", {"value": str(self.ppi) }))

        for bitmap in self.bitmaps:
            strike.append(bitmap.toTTX())

        return strike




class sbix:
    """
    Class representing an sbix table.
    """
    def __init__(self, glyphs):

        self.version = 1 # hard-coded
        self.flags = "00000000 00000001" # hard-coded     TODO: make this data type more accurate.

        # get basic strike information.
        for g in glyphs["img_empty"]:
            if g.img:
                firstGlyphWithStrikes = g
                break

        # iterate over each strike.
        self.strikes = []

        for imageFormat, image in firstGlyphWithStrikes.img.items():
            if imageFormat.split('-')[0] == "png":
                self.strikes.append( sbixStrike(image.strike, glyphs["img_empty"]) )


    def toTTX(self):
        sbix = Element("sbix")

        sbix.append(Element("version", {"value": str(self.version) })) # hard-coded
        sbix.append(Element("flags", {"value": str(self.flags) })) # hard-coded

        for strike in self.strikes:
            sbix.append(strike.toTTX())

        return sbix

#
#
#
#
# def TTXstrike(ppem, resolution, subfolder, glyphs):
#
#
#
#     strike = Element("strike")
#     strike.append(Element("ppem", {"value": str(ppem)}))
#     strike.append(Element("resolution", {"value": resolution}))
#
#
#     for ID, g in enumerate(glyphs["img_empty"]):
#         if not g.img:
#             strike.append(Element("glyph", {"name": g.codepoints.name() }))
#         else:
#             pngElement = Element("glyph",   {"name": g.codepoints.name()
#                                             ,"graphicType": "png "
#                                             ,"originOffsetX": "0"
#                                             ,"originOffsetY": "0"
#                                             })
#             hexdata = Element("hexdata")
#             hexdata.text = g.img[subfolder].getHexDump()
#
#
#             pngElement.append(hexdata)
#             strike.append(pngElement)
#
#     return strike
#
#
#
#
#
# def toTTX(glyphs):
#     """
#     Generates and returns a sbix table with embedded PNG data
#     """
#
#     sbix = Element("sbix")
#
#     sbix.append(Element("version", {"value": "1"})) # hard-coded
#     sbix.append(Element("flags", {"value": "00000000 00000001"})) # hard-coded
#
#
#     # get basic strike information.
#     for g in glyphs["img_empty"]:
#         if g.img:
#             firstGlyphWithStrikes = g
#             break
#
#
#     # iterate over each strike.
#     for imageFormat, image in firstGlyphWithStrikes.img.items():
#         if imageFormat.split('-')[0] == "png":
#             sbix.append(TTXstrike(image.strike, "72", imageFormat, glyphs))
#
#
#
#     return sbix

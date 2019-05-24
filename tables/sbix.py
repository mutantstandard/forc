import struct
from lxml.etree import Element
from data import tag, bFlags



class sbixBitmap:
    """
    Class representing a single bitmap within a strike within an sbix table.
    """
    def __init__(self, glyph, ppem):
        self.name = glyph.name()
        self.originOffsetX = 0 # hard-coded for now
        self.originOffsetY = 0 # hard-coded for now
        self.graphicType = tag("png ") # hard-coded for now

        # forc img class or None
        if glyph.imgDict:
            self.img = glyph.imgDict["png-" + str(ppem)]
        else:
            self.img = None


    def toTTX(self):
        if not self.img:
            return Element("glyph", {"name": self.name })
        else:
            sbixBitmap = Element("glyph",   {"name": self.name
                                            ,"graphicType": str(self.graphicType)
                                            ,"originOffsetX": str(self.originOffsetX)
                                            ,"originOffsetY": str(self.originOffsetY)
                                            })
            hexdata = Element("hexdata")
            hexdata.text = self.img.getHexDump()

            sbixBitmap.append(hexdata)

            return sbixBitmap

    def toBytes(self):
        bitmap = struct.pack( ">hh4b"
                            , self.originOffsetX # Int16
                            , self.originOffsetY # Int16
                            , self.graphicType.toBytes() # Tag (4 bytes/UInt32)
                            )
        # TODO: Add bitmap data:
        # https://docs.microsoft.com/en-gb/typography/opentype/spec/sbix#glyph-data






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


    def toBytes(self):
        strike = struct.pack ( ">HH"
                             , self.ppem # UInt16
                             , self.ppi # UInt16
                             )

        # TODO: add glyphDataOffsets:
        # https://docs.microsoft.com/en-gb/typography/opentype/spec/sbix#strikes




class sbix:
    """
    Class representing an sbix table.
    """
    def __init__(self, glyphs):

        self.version = 1 # hard-coded
        self.flags = bFlags("00000000 00000001") # hard-coded

        self.strikes = []

        # iterate over each strike.
        for imageFormat, image in glyphs["img"][0].imgDict.items():
            if imageFormat.split('-')[0] == "png":
                self.strikes.append( sbixStrike(image.strike, glyphs["img_empty"]) )


    def toTTX(self):
        sbix = Element("sbix")

        sbix.append(Element("version", {"value": str(self.version) })) # hard-coded
        sbix.append(Element("flags", {"value": self.flags.toTTXStr() })) # hard-coded

        for strike in self.strikes:
            sbix.append(strike.toTTX())

        return sbix

    def toBytes(self):
        return struct.pack( ">H2bI"
                          , self.version # UInt16
                          , self.flags.toBytes() # 2 bytes/UInt16
                          , len(self.strikes) # UInt32
                          # TODO: Offsets to each sbix strike.
                          )

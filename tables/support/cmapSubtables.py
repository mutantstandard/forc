from lxml.etree import Element


def makeTTXSubtable(tag, attrs, cmapGlyphSet):
    subtable = Element(tag, attrs)

    for g in cmapGlyphSet:
        if not g.alias:
            subtable.append(Element("map", {"code": hex(g.codepoints.seq[0]), "name": g.name() }))
        else:
            subtable.append(Element("map", {"code": hex(g.codepoints.seq[0]), "name": g.alias.name() }))
    return subtable



class cmapFormat0:
    """
    Class representing cmap subtable format 0.
    (Subtable representing codepoints from U+0 - U+FF.)
    """

    def __init__(self, glyphs, platformID, platEncID, language):

        # check if the glyphs are one-byte, reject them if they are not.
        for g in glyphs:
            if g.codepoints.seq[0] > int('ff', 16):
                raise ValueError(f"Building cmap subtable format 0 failed. A glyph whose codepoint is greater than U+FF was given. cmap Subtable Format 0 must have codepoints less than or equal to U+FF.")

        self.glyphs = glyphs
        self.platformID = platformID
        self.platEncID = platEncID
        self.language = language


    def toTTX(self):
        return makeTTXSubtable(  "cmap_format_0",
                                { "platformID": str(self.platformID)
                                , "platEncID": str(self.platEncID)
                                , "language": str(self.language)
                                }
                                , self.glyphs
                                )


class cmapFormat4:
    """
    Class representing cmap subtable format 4.
    (Subtable representing codepoints from U+0 - U+FFFF.)
    """

    def __init__(self, glyphs, platformID, platEncID, language):

        # check if the glyphs are two-byte, reject them if they are not.
        for g in glyphs:
            if g.codepoints.seq[0] > int('ffff', 16):
                raise ValueError(f"Building cmap subtable format 4 failed. A glyph whose codepoint is greater than U+FFFF was given. cmap Subtable Format 4 must only have codepoints less than or equal to U+FFFF.")

        self.glyphs = glyphs
        self.platformID = platformID
        self.platEncID = platEncID
        self.language = language


    def toTTX(self):
        return makeTTXSubtable(  "cmap_format_4",
                                { "platformID": str(self.platformID)
                                , "platEncID": str(self.platEncID)
                                , "language": str(self.language)
                                }
                                , self.glyphs
                                )


class cmapFormat12:
    """
    Class representing cmap subtable format 12.
    (Subtable representing codepoints from U+0 - U+FFFFFF.)
    """

    def __init__(self, glyphs, platformID, platEncID, language):

        # check if the glyphs are four-byte, reject them if they are not.
        for g in glyphs:
            if g.codepoints.seq[0] > int('ffffff', 16):
                raise ValueError(f"Building cmap subtable format 12 failed. A glyph whose codepoint is greater than U+FFFFFF was given. cmap Subtable Format 12 must only have codepoints less than or equal to U+FFFFFF.")

        self.glyphs = glyphs
        self.platformID = platformID
        self.platEncID = platEncID
        self.language = language


    def toTTX(self):
        return makeTTXSubtable(  "cmap_format_12",
                                { "platformID": str(self.platformID)
                                , "platEncID": str(self.platEncID)
                                , "language": str(self.language)
                                , "format": "12"
                                , "reserved": "0"
                                , "length": "0"
                                , "nGroups": "0"
                                }
                                , self.glyphs
                                )




class cmapFormat14:
    """
    Class representing cmap subtable format 14.
    (Subtable indicating the usage of variation selectors.)

    This is only capable of implementing Variation Selector 16 (U+FE0F) right now.
    """

    def __init__(self, glyphs, platformID, platEncID):
        self.glyphs = glyphs
        self.platformID = platformID
        self.platEncID = platEncID


    def toTTX(self):
        cmap14 = Element("cmap_format_14",    { "platformID": str(self.platformID)
                                                , "platEncID": str(self.platEncID)
                                                , "format": "14"
                                                , "length": "0"
                                                , "numVarSelectorRecords": "1"
                                                })

        for g in self.glyphs:
            if not g.alias:
                cmap14.append(Element("map", {"uvs": "0xfe0f", "uv": hex(g.codepoints.seq[0]), "name": g.name()}))
            else:
                cmap14.append(Element("map", {"uvs": "0xfe0f", "uv": hex(g.codepoints.seq[0]), "name": g.alias.name()}))

        return cmap14

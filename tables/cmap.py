from lxml.etree import Element



def makeGlyphSubtable(tag, attrs, cmapGlyphSet):
    subtable = Element(tag, attrs)

    for g in cmapGlyphSet:
        if not g.alias:
            subtable.append(Element("map", {"code": hex(g.codepoints.seq[0]), "name": g.codepoints.name() }))
        else:
            subtable.append(Element("map", {"code": hex(g.codepoints.seq[0]), "name": g.alias.name() }))
    return subtable






def cmap(glyphs):
    cmap = Element("cmap")
    cmap.append(Element("tableVersion", {"version": "0"}))


    # check what's what in this set to determine what subtables to create.
    # ---------------------------------------------------------
    vs16Presence = False
    oneByte = []
    twoByte = []
    fourByte = []

    for g in glyphs['all']:
        if g.vs16:
            vs16Presence = True

        if len(g) == 1:
            if g.codepoints.seq[0] < int('ff', 16):
                oneByte.append(g)
            if g.codepoints.seq[0] < int('ffff', 16):
                twoByte.append(g)
            if g.codepoints.seq[0] < int('ffffff', 16):
                fourByte.append(g)


    # cmap 0
    # U+0 - U+FF
    # ---------------------------------------------------------

    if oneByte:
        cmap.append(makeGlyphSubtable(  "cmap_format_0",
                                            { "platformID": "1"
                                            , "platEncID": "0"
                                            , "language": "0"
                                            }
                                        , oneByte
                                        ))



    # cmap 4
    # U+0 - U+FFFF
    # ---------------------------------------------------------

    if twoByte:

        # platform ID 0 (Unicode)
        cmap.append(makeGlyphSubtable(  "cmap_format_4",
                                            { "platformID": "0"
                                            , "platEncID": "3"
                                            , "language": "0"
                                            }
                                        , twoByte
                                        ))



        # platform ID 3 (Microsoft)

        # platEncID should be 1. This is what is required to make
        # this particular cmap subtable format work.
        cmap.append(makeGlyphSubtable(  "cmap_format_4",
                                            { "platformID": "3"
                                            , "platEncID": "1" #necessary
                                            , "language": "0"
                                            }
                                        , twoByte
                                        ))




    # cmap 12
    # U+0 - U+FFFFFF
    # ---------------------------------------------------------

    if fourByte:

        # platform ID 0 (Unicode)
        cmap.append(makeGlyphSubtable(  "cmap_format_12",
                                            { "platformID": "0"
                                            , "platEncID": "10"
                                            , "language": "0"
                                            , "format": "12"
                                            , "reserved": "0"
                                            , "length": "0"
                                            , "nGroups": "0"
                                            }
                                        , fourByte
                                        ))


        # platform ID 3 (Microsoft)

        # platEncID should be 10. This is what is required to make
        # this particular cmap subtable format work.
        cmap.append(makeGlyphSubtable(  "cmap_format_12",
                                            { "platformID": "3"
                                            , "platEncID": "10" #necessary
                                            , "language": "0"
                                            , "format": "12"
                                            , "reserved": "0"
                                            , "length": "0"
                                            , "nGroups": "0"
                                            }
                                        , fourByte
                                        ))




    # cmap 14 (if vs16 is used in the glyph set)
    # ---------------------------------------------------------

    if vs16Presence:
        cmap14_1 = Element("cmap_format_14",    { "platformID": "0"
                                                , "platEncID": "5"
                                                , "format": "14"
                                                , "length": "0"
                                                , "numVarSelectorRecords": "1"
                                                })

        for g in glyphs['all']:
            if g.vs16:
                cmap14_1.append(Element("map", {"uvs": "0xfe0f", "uv": hex(g.codepoints.seq[0]), "name": "None"}))

        cmap.append(cmap14_1)




    return cmap

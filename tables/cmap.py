from lxml.etree import Element



def cmap(glyphs):
    cmap = Element("cmap")
    cmap.append(Element("tableVersion", {"version": "0"}))


    # check what's what in this set to determine what subtables to create.
    # ---------------------------------------------------------
    vs16Presence = False
    oneByte = []
    twoByte = []
    fourByte = []

    for g in glyphs:
        if g.vs16:
            vs16Presence = True

        if len(g.codepoints) == 1:
            #if g.codepoints[0] < int('ff', 16):
                #oneByte.append(g)
            if g.codepoints[0] < int('ffff', 16):
                twoByte.append(g)
            if g.codepoints[0] < int('ffffff', 16):
                fourByte.append(g)


    # cmap 0
    # U+0 - U+FF
    # ---------------------------------------------------------

    if oneByte:
        cmap0 = Element("cmap_format_0",    { "platformID": "1"
                                            , "platEncID": "0"
                                            , "language": "0"
                                            })

        for g in oneByte:
            cmap0.append(Element("map", {"code": hex(g.codepoints[0]), "name": g.name}))

        cmap.append(cmap0)



    # cmap 4
    # U+0 - U+FFFF
    # ---------------------------------------------------------

    if twoByte:

        # platform ID 0 (Unicode)
        cmap4_0 = Element("cmap_format_4",    { "platformID": "0"
                                                , "platEncID": "3"
                                                , "language": "0"
                                                })
        for g in twoByte:
            cmap4_0.append(Element("map", {"code": hex(g.codepoints[0]), "name": g.name}))

        cmap.append(cmap4_0)



        # platform ID 3 (Microsoft)
        cmap4_3 = Element("cmap_format_4",    { "platformID": "3"
                                                , "platEncID": "1"
                                                , "language": "0"
                                                })
        for g in twoByte:
            cmap4_3.append(Element("map", {"code": hex(g.codepoints[0]), "name": g.name}))

        cmap.append(cmap4_3)





    # cmap 12
    # U+0 - U+FFFFFF
    # ---------------------------------------------------------

    if fourByte:

        # platform ID 0 (Unicode)
        cmap12_1 = Element("cmap_format_12",    { "platformID": "0"
                                                , "platEncID": "10"
                                                , "language": "0"
                                                , "format": "12"
                                                , "reserved": "0"
                                                , "length": "0"
                                                , "nGroups": "0"
                                                })
        for g in fourByte:
            cmap12_1.append(Element("map", {"code": hex(g.codepoints[0]), "name": g.name}))

        cmap.append(cmap12_1)



        # platform ID 3 (Microsoft)
        cmap12_3 = Element("cmap_format_12",    { "platformID": "3"
                                                , "platEncID": "1"
                                                , "language": "0"
                                                , "format": "12"
                                                , "reserved": "0"
                                                , "length": "0"
                                                , "nGroups": "0"
                                                })

        for g in fourByte:
            cmap12_3.append(Element("map", {"code": hex(g.codepoints[0]), "name": g.name}))

        cmap.append(cmap12_3)





    # cmap 14 (if vs16 is used in the glyph set)
    # ---------------------------------------------------------

    if vs16Presence:
        cmap14_1 = Element("cmap_format_14",    { "platformID": "0"
                                                , "platEncID": "5"
                                                , "format": "14"
                                                , "length": "0"
                                                , "numVarSelectorRecords": "1"
                                                })

        for g in glyphs:
            if g.vs16:
                cmap14_1.append(Element("map", {"uvs": "0xfe0f", "uv": hex(g.codepoints[0]), "name": "None"}))

        cmap.append(cmap14_1)




    return cmap

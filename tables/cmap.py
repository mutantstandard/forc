from lxml.etree import Element



def cmap(macLangID, msftLangID, glyphs):
    cmap = Element("cmap")
    cmap.append(Element("tableVersion", {"version": "0"}))



    # cmap 12, enc 0
    # ---------------------------------------------------------

    cmap12_1 = Element("cmap_format_12",    { "platformID": "0"
                                            , "platEncID": "0"
                                            , "language": "0"
                                            , "format": "12"
                                            , "reserved": "0"
                                            , "length": "0"
                                            , "nGroups": "0"
                                            })
    for g in glyphs:
        if len(g.codepoints) == 1:
            cmap12_1.append(Element("map", {"code": hex(g.codepoints[0]), "name": g.name}))

    cmap.append(cmap12_1)





    # cmap 12, enc 3
    # ---------------------------------------------------------

    cmap12_2 = Element("cmap_format_12",    { "platformID": "3"
                                            , "platEncID": "1"
                                            , "language": msftLangID
                                            , "format": "12"
                                            , "reserved": "0"
                                            , "length": "0"
                                            , "nGroups": "0"
                                            })

    for g in glyphs:
        if len(g.codepoints) == 1:
            cmap12_2.append(Element("map", {"code": hex(g.codepoints[0]), "name": g.name}))

    cmap.append(cmap12_2)





    # cmap 14 (if vs16 is used in the glyph set)
    # ---------------------------------------------------------

    vs16Presence = False

    for g in glyphs:
        if g.vs16:
            vs16Presence = True

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

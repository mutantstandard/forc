from lxml.etree import Element





def cmap(macLangID, msftLangID, glyphs):




    cmap = Element("cmap")

    cmap.append(Element("tableVersion", {"version": "0"}))

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

    return cmap

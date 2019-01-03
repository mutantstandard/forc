from xml.etree.ElementTree import Element

def cmap(macLangID, msftLangID):
    cmap = Element("cmap")

    cmap.append(Element("tableVersion", {"version": "0"}))

    cmap12_1 = Element("cmap_format_12",   { "platEncID": "0"
                                            , "language": "0"
                                            , "format": "12"
                                            , "reserved": "0"
                                            , "length": "0"
                                            , "nGroupd": "0"
                                            })
    # fill it with goodies here
    cmap.append(cmap12_1)

    cmap12_2 = Element("cmap_format_12",   { "platEncID": "1"
                                            , "language": msftLangID
                                            , "format": "12"
                                            , "reserved": "0"
                                            , "length": "0"
                                            , "nGroupd": "0"
                                            })
    # fill it with goodies here
    cmap.append(cmap12_2)

    return cmap

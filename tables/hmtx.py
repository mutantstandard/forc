from lxml.etree import Element

def toTTX(m, glyphs):
    metrics = m['metrics']

    hmtx = Element("hmtx")

    for g in glyphs["img_empty"]:
        hmtx.append(Element("mtx", {"name": g.codepoints.name()
                                    ,"width": str(metrics['normalWidth'])
                                    ,"lsb": str(metrics['normalLSB'])
                                    }))

    return hmtx

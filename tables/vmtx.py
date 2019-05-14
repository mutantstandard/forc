from lxml.etree import Element

def toTTX(m, glyphs):
    metrics = m['metrics']

    vmtx = Element("vmtx")

    for g in glyphs["img_empty"]:
        vmtx.append(Element("mtx", {"name": g.codepoints.name()
                                    ,"height": str(metrics['normalHeight'])
                                    ,"tsb": str(metrics['normalTSB'])
                                    }))

    return vmtx

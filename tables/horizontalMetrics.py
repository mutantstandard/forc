from lxml.etree import Element

def hhea(metrics):
    hhea = Element("hhea")

    hhea.append(Element("tableVersion", {'value': '0x00010000'})) # hard-coded

    hhea.append(Element("ascent", {'value': str(metrics['yMax']) }))
    hhea.append(Element("descent", {'value': str(metrics['yMin']) }))
    hhea.append(Element("lineGap", {'value': "0" })) # hard-coded based on best practices

    hhea.append(Element("advanceWidthMax", {'value': '2048'}))
    hhea.append(Element("minLeftSideBearing", {'value': '0'}))
    hhea.append(Element("minRightSideBearing", {'value': '0'}))
    hhea.append(Element("xMaxExtent", {'value': '2048'}))

    hhea.append(Element("caretSlopeRise", {'value': '1'})) # probably hard-coded
    hhea.append(Element("caretSlopeRun", {'value': '0'})) # probably hard-coded
    hhea.append(Element("caretOffset", {'value': '0'})) # probably hard-coded

    hhea.append(Element("reserved0", {'value': '0'})) # hard-coded
    hhea.append(Element("reserved1", {'value': '0'})) # hard-coded
    hhea.append(Element("reserved2", {'value': '0'})) # hard-coded
    hhea.append(Element("reserved3", {'value': '0'})) # hard-coded

    hhea.append(Element("metricDataFormat", {'value': '0'})) # hard-coded
    hhea.append(Element("numberOfHMetrics", {'value': '0'})) # maybe TTX auto-denerates this?

    return hhea


def hmtx(metrics, glyphs):
    hmtx = Element("hmtx")

    for g in glyphs:
        if g.name is 'space':
            hmtx.append(Element("mtx",  {"name": g.name
                                        ,"width": str(metrics['spaceHLength'])
                                        ,"lsb": str(metrics['normalLSB'])
                                        }))
        elif g.name is 'CR':
            hmtx.append(Element("mtx", {"name": g.name
                                        ,"width": "0"
                                        ,"lsb": "0"
                                        }))
        else:
            hmtx.append(Element("mtx", {"name": g.name
                                        ,"width": str(metrics['normalWidth'])
                                        ,"lsb": str(metrics['normalLSB'])
                                        }))

    return hmtx

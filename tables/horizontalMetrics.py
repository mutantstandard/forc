from xml.etree.ElementTree import Element

def hhea():
    hhea = Element("hhea")

    hhea.append(Element("tableVersion", {'value': '0x00010000'})) # hard-coded

    hhea.append(Element("ascent", {'value': '1578'}))
    hhea.append(Element("descent", {'value': '-470'}))
    hhea.append(Element("lineGap", {'value': '0'}))

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


def hmtx():
    hmtx = Element("hmtx")

    return hmtx

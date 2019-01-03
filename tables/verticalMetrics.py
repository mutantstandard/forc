from xml.etree.ElementTree import Element

def vhea():
    vhea = Element("vhea")

    vhea.append(Element("tableVersion", {'value': '0x00010000'}))  # hard-coded

    vhea.append(Element("ascent", {'value': '1578'}))
    vhea.append(Element("descent", {'value': '-470'}))
    vhea.append(Element("lineGap", {'value': '0'}))

    vhea.append(Element("advanceHeightMax", {'value': '2048'}))
    vhea.append(Element("minTopSideBearing", {'value': '0'}))
    vhea.append(Element("minBottomSideBearing", {'value': '0'}))
    vhea.append(Element("yMaxExtent", {'value': '2048'}))

    vhea.append(Element("caretSlopeRise", {'value': '1'})) # probably hard-coded
    vhea.append(Element("caretSlopeRun", {'value': '0'})) # probably hard-coded
    vhea.append(Element("caretOffset", {'value': '0'})) # probably hard-coded

    ## yes, this is different from vhea. tables are weird.
    vhea.append(Element("reserved1", {'value': '0'})) # hard-coded
    vhea.append(Element("reserved2", {'value': '0'})) # hard-coded
    vhea.append(Element("reserved3", {'value': '0'})) # hard-coded
    vhea.append(Element("reserved4", {'value': '0'})) # hard-coded

    vhea.append(Element("metricDataFormat", {'value': '0'})) # hard-coded
    vhea.append(Element("numberOfHMetrics", {'value': '0'})) # maybe TTX auto-denerates this?

    return vhea


def vmtx():
    vmtx = Element("vmtx")

    return vmtx

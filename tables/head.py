from xml.etree.ElementTree import Element

def head():
    head = Element("head")

    head.append(Element("tableVersion", {'value': '1.0'})) # hard-coded
    head.append(Element("fontRevision", {'value': '0.0'}))

    head.append(Element("checkSumAdjustment", {'value': '0'})) # TTX changes this at compilation
    head.append(Element("magicNumber", {'value': '0x5f0f3cf5'})) # hard-coded

    head.append(Element("flags", {'value': '00000000 00001011'})) # hard-coded

    head.append(Element("created", {'value': 'Mon Dec 11 13:45:00 2018'}))
    head.append(Element("modified", {'value': 'Mon Dec 11 13:45:00 2018'})) # TTX changes this at compilation

    head.append(Element("xMin", {'value': '1.0'}))
    head.append(Element("yMin", {'value': '1.0'}))
    head.append(Element("xMax", {'value': '1.0'}))
    head.append(Element("yMax", {'value': '1.0'}))

    head.append(Element("macStyle", {'value': '00000000 00000000'})) # hard-coded. Must agree with os2's fsType.
    head.append(Element("lowestRecPPEM", {'value': '16'}))

    head.append(Element("indexToLocFormat", {'value': '0'})) # not important, hard-coded
    head.append(Element("glyphDataFormat", {'value': '0'})) # not important, hard-coded

    return head

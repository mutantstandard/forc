from xml.etree.ElementTree import Element

def head(metrics, created):
    head = Element("head")

    head.append(Element("tableVersion", {'value': '1.0'})) # hard-coded
    head.append(Element("fontRevision", {'value': '0.0'}))

    head.append(Element("checkSumAdjustment", {'value': '0'})) # TTX changes this at compilation
    head.append(Element("magicNumber", {'value': '0x5f0f3cf5'})) # hard-coded

    head.append(Element("flags", {'value': '00000000 00001011'})) # hard-coded

    head.append(Element("created", {'value': created}))
    head.append(Element("modified", {'value': 'Mon Dec 11 13:45:00 2018'})) # TTX changes this at compilation

    head.append(Element("xMin", {'value': str(metrics['xMin']) }))
    head.append(Element("yMin", {'value': str(metrics['yMin']) }))
    head.append(Element("xMax", {'value': str(metrics['xMax']) }))
    head.append(Element("yMax", {'value': str(metrics['yMax']) }))

    head.append(Element("macStyle", {'value': '00000000 00000000'})) # hard-coded. Must agree with os2's fsType.
    head.append(Element("lowestRecPPEM", {'value': str(metrics['lowestRecPPEM']) }))

    head.append(Element("indexToLocFormat", {'value': '0'})) # not important, hard-coded
    head.append(Element("glyphDataFormat", {'value': '0'})) # not important, hard-coded

    return head

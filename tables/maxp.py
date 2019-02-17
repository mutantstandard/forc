from lxml.etree import Element

def maxp():
    """
    Create a maxp table. All of the data inside this is dummy data, the TTX
    compiler will insert actually useful data.
    """

    maxp = Element("maxp")

    maxp.append(Element("tableVersion", {'value': '0x10000'})) # hard-coded
    maxp.append(Element("numGlyphs", {'value': '0'}))
    maxp.append(Element("maxPoints", {'value': '0'}))
    maxp.append(Element("maxContours", {'value': '0'}))
    maxp.append(Element("maxCompositePoints", {'value': '0'}))
    maxp.append(Element("maxCompositeContours", {'value': '0'}))
    maxp.append(Element("maxZones", {'value': '0'}))
    maxp.append(Element("maxTwilightPoints", {'value': '0'}))
    maxp.append(Element("maxStorage", {'value': '1'}))
    maxp.append(Element("maxFunctionDefs", {'value': '1'}))
    maxp.append(Element("maxInstructionDefs", {'value': '0'}))
    maxp.append(Element("maxStackElements", {'value': '64'}))
    maxp.append(Element("maxSizeOfInstructions", {'value': '0'}))
    maxp.append(Element("maxComponentElements", {'value': '0'}))
    maxp.append(Element("maxComponentDepth", {'value': '0'}))

    return maxp

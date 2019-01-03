from xml.etree.ElementTree import Element

def sbix():
    """
    Generates and returns a sbix table with embedded PNG data
    """
    sbix = Element("sbix")

    sbix.append(Element("version", {"value": "1"})) # hard-coded
    sbix.append(Element("flags", {"value": "00000000 00000001"})) # hard-coded

    # for each strike
    # (this is all test data)
    strike1 = Element("strike")
    strike1.append(Element("ppem", {"Value": "128"}))
    strike1.append(Element("resolution", {"value": "72"}))

    # glyphs for this particular strike begin now

    # here you will need to add all of the juicy glyphs.
    # for each blah blah
    #   svgElement = Element("glyph", {"startGlyph": ID, "endGlyph" : ID})
    #   - check if it's meant to be blank (ie is CR or space)
    #   - if not, put this in:
    # stuff the edited SVG into CDATA.

    sbix.append(strike1)


    return sbix

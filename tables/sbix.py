from lxml.etree import Element

def sbix(glyphs):
    """
    Generates and returns a sbix table with embedded PNG data
    """

    sbix = Element("sbix")

    sbix.append(Element("version", {"value": "1"})) # hard-coded
    sbix.append(Element("flags", {"value": "00000000 00000001"})) # hard-coded



    # for each strike
    # (for now, we are just creating 1 strike manually)
    strike1 = Element("strike")
    strike1.append(Element("ppem", {"value": "128"}))
    strike1.append(Element("resolution", {"value": "72"}))

    for ID, g in enumerate(glyphs):
        if not g.imagePath:
            strike1.append(Element("glyph", {"name": g.name }))
        else:
            pngElement = Element("glyph",   {"name": g.name
                                            ,"graphicType": "png "
                                            ,"originOffsetX": "0"
                                            ,"originOffsetY": "0"
                                            })
            hexdata = Element("hexdata")

            with open(g.imagePath, "rb") as read_file:
                pngHexdump = read_file.read().hex()

            hexdata.text = pngHexdump

            # get the png, make it Base64.
            # hexdata.text

            pngElement.append(hexdata)
            strike1.append(pngElement)

    # glyphs for this particular strike begin now

    # here you will need to add all of the juicy glyphs.
    # for each blah blah
    #   svgElement = Element("glyph", {"startGlyph": ID, "endGlyph" : ID})
    #   - check if it's meant to be blank (ie is CR or space)
    #   - if not, put this in:
    # stuff the edited SVG into CDATA.

    sbix.append(strike1)


    return sbix

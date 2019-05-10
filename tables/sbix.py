from lxml.etree import Element



def strike(ppem, resolution, subfolder, glyphs):
    strike = Element("strike")
    strike.append(Element("ppem", {"value": str(ppem)}))
    strike.append(Element("resolution", {"value": resolution}))


    for ID, g in enumerate(glyphs['img']):
        if not g.img:
            strike.append(Element("glyph", {"name": g.codepoints.name() }))
        else:
            pngElement = Element("glyph",   {"name": g.codepoints.name()
                                            ,"graphicType": "png "
                                            ,"originOffsetX": "0"
                                            ,"originOffsetY": "0"
                                            })
            hexdata = Element("hexdata")
            hexdata.text = g.img[subfolder].getHexDump()


            pngElement.append(hexdata)
            strike.append(pngElement)

    return strike





def create(glyphs):
    """
    Generates and returns a sbix table with embedded PNG data
    """

    sbix = Element("sbix")

    sbix.append(Element("version", {"value": "1"})) # hard-coded
    sbix.append(Element("flags", {"value": "00000000 00000001"})) # hard-coded


    # get basic strike information.
    for g in glyphs['img']:
        if g.img:
            firstGlyphWithStrikes = g
            break


    # iterate over each strike.
    for imageFormat, image in firstGlyphWithStrikes.img.items():
        if imageFormat.split('-')[0] == "png":
            sbix.append(strike(image.strike, "72", imageFormat, glyphs))



    return sbix

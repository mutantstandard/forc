from lxml.etree import Element



def strike(metrics, strikeIndex, strikeRes, subfolder, glyphs):
    # start of strikes
    # (which we're fudging right now)
    # ------------------------------------------------------------
    strike = Element("strikedata", {"index": strikeIndex})

    for g in glyphs:

        # you only put them in if there's an actual image
        if g.imagePath:
            bitmapTable = Element("cbdt_bitmap_format_17", {"name": g.name})

            smallGlyphMetrics = Element("SmallGlyphMetrics")
            smallGlyphMetrics.append(Element("height", {"value": "0"}))
            smallGlyphMetrics.append(Element("width", {"value": "0"}))
            smallGlyphMetrics.append(Element("BearingX", {"value": "0"}))
            smallGlyphMetrics.append(Element("BearingY", {"value": "0"}))
            smallGlyphMetrics.append(Element("Advance", {"value": "0"}))

            bitmapTable.append(smallGlyphMetrics)


            rawImageData = Element("rawimagedata")

            with open(g.imagePath[subfolder], "rb") as read_file:
                pngHexdump = read_file.read().hex()

            rawImageData.text = pngHexdump

            bitmapTable.append(rawImageData)

            strike.append(bitmapTable)

    return strike




def cbdt(metrics, glyphs):
    """
    Generates and returns a glyf table with dummy data.
    """

    cbdt = Element("CBDT")

    cbdt.append(Element("header", {"version": "3.0"})) # hard-coded



    # get basic strike information.

    for g in glyphs:
        if g.imagePath:
            firstGlyphWithStrikes = g
            break


    # iterate over each strike.

    strikeIndex = 0

    for formatName, format in firstGlyphWithStrikes.imagePath.items():
        if formatName.split('-')[0] == "png":
            strikeRes = formatName.split('-')[1]
            cbdt.append(strike(metrics, str(strikeIndex), strikeRes, formatName, glyphs))
            strikeIndex += 1



    return cbdt

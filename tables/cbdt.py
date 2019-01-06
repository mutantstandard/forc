from xml.etree.ElementTree import Element

def cbdt(metrics, glyphs):
    """
    Generates and returns a glyf table with dummy data.
    """

    cbdt = Element("CBDT")

    cbdt.append(Element("header", {"version": "3.0"})) # hard-coded




    # start of strikes
    # (which we're fudging right now)
    # ------------------------------------------------------------
    strike = Element("strikedata", {"index": "0"})

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

            with open(g.imagePath, "rb") as read_file:
                pngHexdump = read_file.read().hex()

            rawImageData.text = pngHexdump

            bitmapTable.append(rawImageData)

            strike.append(bitmapTable)

    cbdt.append(strike)


    return cbdt

from lxml.etree import Element



def strike(metrics, strikeIndex, ppem, glyphs):
        # start of strikes
        # (which we're fudging right now)
        # ------------------------------------------------------------
        strike = Element("strike", {"index": strikeIndex})



        # bitmapSizeTable
        # --------------------------------

        bSizeTable = Element("bitmapSizeTable")

        horizontalMetrics = Element("sbitLineMetrics", {"direction": "hori"})
        horizontalMetrics.append(Element("ascender", {"value": "0"}))
        horizontalMetrics.append(Element("descender", {"value": "0"}))
        horizontalMetrics.append(Element("widthMax", {"value": "0" }))

        horizontalMetrics.append(Element("caretSlopeNumerator", {"value": "0"}))
        horizontalMetrics.append(Element("caretSlopeDenominator", {"value": "0"}))
        horizontalMetrics.append(Element("caretOffset", {"value": "0"}))

        horizontalMetrics.append(Element("minOriginSB", {"value": "0"}))
        horizontalMetrics.append(Element("minAdvanceSB", {"value": "0" }))

        horizontalMetrics.append(Element("maxBeforeBL", {"value": "0"}))
        horizontalMetrics.append(Element("minAfterBL", {"value": "0" }))
        horizontalMetrics.append(Element("pad1", {"value": "0"}))
        horizontalMetrics.append(Element("pad2", {"value": "0"}))

        bSizeTable.append(horizontalMetrics)

        verticalMetrics = Element("sbitLineMetrics", {"direction": "vert"})
        verticalMetrics.append(Element("ascender", {"value": "0"}))
        verticalMetrics.append(Element("descender", {"value": "0"}))
        verticalMetrics.append(Element("widthMax", {"value": "0" }))

        verticalMetrics.append(Element("caretSlopeNumerator", {"value": "0"}))
        verticalMetrics.append(Element("caretSlopeDenominator", {"value": "0"}))
        verticalMetrics.append(Element("caretOffset", {"value": "0"}))

        verticalMetrics.append(Element("minOriginSB", {"value": "0"}))
        verticalMetrics.append(Element("minAdvanceSB", {"value": "0" }))

        verticalMetrics.append(Element("maxBeforeBL", {"value": "0"}))
        verticalMetrics.append(Element("minAfterBL", {"value": "0" }))
        verticalMetrics.append(Element("pad1", {"value": "0"}))
        verticalMetrics.append(Element("pad2", {"value": "0"}))

        bSizeTable.append(verticalMetrics)

        bSizeTable.append(Element("colorRef", {"value": "0"}))

        bSizeTable.append(Element("startGlyphIndex", {"value": "0"}))
        bSizeTable.append(Element("endGlyphIndex", {"value": "0"}))

        bSizeTable.append(Element("ppemX", {"value": "128"}))
        bSizeTable.append(Element("ppemY", {"value": "128"}))

        bSizeTable.append(Element("bitDepth", {"value": "32"}))
        bSizeTable.append(Element("flags", {"value": "1"}))

        strike.append(bSizeTable)

        eblcSub = Element("eblc_index_sub_table_1", {"imageFormat": "17"})

        # EBLC index subtable
        # --------------------------------

        glyphIDList = []

        for id, g in enumerate(glyphs):

            # you only put them in if there's an actual image
            if g.imagePath:
                glyphIDList.append(id)
                eblcSub.append(Element("glyphLoc", {"id": str(id), "name": g.name}))

        eblcSub.attrib['firstGlyphIndex'] = str(glyphIDList[0])
        eblcSub.attrib['lastGlyphIndex'] = str(glyphIDList[-1])
        bSizeTable.attrib['firstGlyphIndex'] = str(glyphIDList[0])
        bSizeTable.attrib['lastGlyphIndex'] = str(glyphIDList[0])

        strike.append(eblcSub)

        return strike





def cblc(metrics, glyphs):
    """
    Generates and returns a glyf table with dummy data.
    """

    cblc = Element("CBLC")

    cblc.append(Element("header", {"version": "3.0"})) # hard-coded



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
            cblc.append(strike(metrics, str(strikeIndex), strikeRes, glyphs))
            strikeIndex += 1




    return cblc

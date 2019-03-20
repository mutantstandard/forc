from lxml.etree import Element



def strike(metrics, strikeIndex, ppem, glyphs):




        # metrics in CBLC/EBLC tables are done as 8-bit integers (which are signed, apart from widthMax).
        # the key to handling CBLC/EBLC metrics is to make the numbers small and proportional enough to fit into this.



        horiAscender =  round( (metrics['yMax'] / metrics['unitsPerEm']) * 128 )
        horiDescender = round( (metrics['yMin'] / metrics['unitsPerEm']) * 128 )
        horiWidthMax =  round( (metrics['width'] / metrics['unitsPerEm']) * 128 )

        vertAscender = horiAscender
        vertDescender = horiDescender
        vertWidthMax = horiWidthMax



        strike = Element("strike", {"index": str(strikeIndex)})



        # bitmapSizeTable
        # --------------------------------

        bSizeTable = Element("bitmapSizeTable")



        # horizontal metrics

        horizontalMetrics = Element("sbitLineMetrics", {"direction": "hori"})

        horizontalMetrics.append(Element("ascender", {"value": str(horiAscender) }))
        horizontalMetrics.append(Element("descender", {"value": str(horiDescender) }))
        horizontalMetrics.append(Element("widthMax", {"value": str(horiWidthMax) }))

        horizontalMetrics.append(Element("caretSlopeNumerator", {"value": "0"}))    # hard-coded
        horizontalMetrics.append(Element("caretSlopeDenominator", {"value": "0"}))  # hard-coded
        horizontalMetrics.append(Element("caretOffset", {"value": "0"}))            # hard-coded

        horizontalMetrics.append(Element("minOriginSB", {"value": "0"}))
        horizontalMetrics.append(Element("minAdvanceSB", {"value": "0" }))

        horizontalMetrics.append(Element("maxBeforeBL", {"value": "0"}))
        horizontalMetrics.append(Element("minAfterBL", {"value": "0" }))
        horizontalMetrics.append(Element("pad1", {"value": "0"}))
        horizontalMetrics.append(Element("pad2", {"value": "0"}))

        bSizeTable.append(horizontalMetrics)





        # vertical metrics

        verticalMetrics = Element("sbitLineMetrics", {"direction": "vert"})

        verticalMetrics.append(Element("ascender", {"value": str(vertAscender) }))
        verticalMetrics.append(Element("descender", {"value": str(vertDescender) }))
        verticalMetrics.append(Element("widthMax", {"value": str(vertWidthMax) }))

        verticalMetrics.append(Element("caretSlopeNumerator", {"value": "0"}))      # hard-coded
        verticalMetrics.append(Element("caretSlopeDenominator", {"value": "0"}))    # hard-coded
        verticalMetrics.append(Element("caretOffset", {"value": "0"}))              # hard-coded

        verticalMetrics.append(Element("minOriginSB", {"value": "0"}))
        verticalMetrics.append(Element("minAdvanceSB", {"value": "0" }))

        verticalMetrics.append(Element("maxBeforeBL", {"value": "0"}))
        verticalMetrics.append(Element("minAfterBL", {"value": "0" }))
        verticalMetrics.append(Element("pad1", {"value": "0"}))
        verticalMetrics.append(Element("pad2", {"value": "0"}))

        bSizeTable.append(verticalMetrics)




        # other stuff

        bSizeTable.append(Element("colorRef", {"value": "0"}))

        bSizeTable.append(Element("startGlyphIndex", {"value": "0"}))
        bSizeTable.append(Element("endGlyphIndex", {"value": "0"}))

        bSizeTable.append(Element("ppemX", {"value": str(ppem) }))
        bSizeTable.append(Element("ppemY", {"value": str(ppem) }))

        bSizeTable.append(Element("bitDepth", {"value": "32"}))
        bSizeTable.append(Element("flags", {"value": "1"}))

        strike.append(bSizeTable)

        eblcSub = Element("eblc_index_sub_table_1", {"imageFormat": "17"})





        # EBLC index subtable
        # --------------------------------

        glyphIDList = []

        for id, g in enumerate(glyphs['img']):

            # you only put them in if there's an actual image
            if g.imagePath:
                glyphIDList.append(id)
                eblcSub.append(Element("glyphLoc", {"id": str(id), "name": g.codepoints.name() }))

        eblcSub.attrib['firstGlyphIndex'] = str(glyphIDList[0])
        eblcSub.attrib['lastGlyphIndex'] = str(glyphIDList[-1])
        bSizeTable.attrib['firstGlyphIndex'] = str(glyphIDList[0])
        bSizeTable.attrib['lastGlyphIndex'] = str(glyphIDList[0])

        strike.append(eblcSub)

        return strike





def create(m, glyphs):
    """
    Generates and returns a glyf table with dummy data.
    """

    metrics = m['metrics']

    cblc = Element("CBLC")

    cblc.append(Element("header", {"version": "3.0"})) # hard-coded



    # get basic strike information.

    for g in glyphs['img']:
        if g.imagePath:
            firstGlyphWithStrikes = g
            break


    # iterate over each strike.

    strikeIndex = 0

    for imageFormat, image in firstGlyphWithStrikes.imagePath.items():
        if imageFormat.split('-')[0] == "png":
            cblc.append(strike(metrics, strikeIndex, image.strike, glyphs))
            strikeIndex += 1




    return cblc

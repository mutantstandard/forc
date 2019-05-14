from lxml.etree import Element
from tables.support.eblc_ebdt_metrics import sbitLineMetricsHori, sbitLineMetricsVert


def strike(metrics, strikeIndex, ppem, glyphs):

    strike = Element("strike", {"index": str(strikeIndex)})


    # bitmapSizeTable
    # --------------------------------

    bSizeTable = Element("bitmapSizeTable")

    bSizeTable.append(sbitLineMetricsHori(metrics))
    bSizeTable.append(sbitLineMetricsVert(metrics))



    # other stuff
    # --------------------------------
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

    for id, g in enumerate(glyphs["img_empty"]):

        # you only put them in if there's an actual image
        if g.imgDict:
            glyphIDList.append(id)
            eblcSub.append(Element("glyphLoc", {"id": str(id), "name": g.codepoints.name() }))

    eblcSub.attrib['firstGlyphIndex'] = str(glyphIDList[0])
    eblcSub.attrib['lastGlyphIndex'] = str(glyphIDList[-1])
    bSizeTable.attrib['firstGlyphIndex'] = str(glyphIDList[0])
    bSizeTable.attrib['lastGlyphIndex'] = str(glyphIDList[0])

    strike.append(eblcSub)

    return strike





def toTTX(m, glyphs):
    """
    Generates and returns a glyf table with dummy data.
    """

    metrics = m['metrics']

    cblc = Element("CBLC")

    cblc.append(Element("header", {"version": "3.0"})) # hard-coded



    # get basic strike information.

    for g in glyphs["img_empty"]:
        if g.imgDict:
            firstGlyphWithStrikes = g
            break


    # iterate over each strike.

    strikeIndex = 0

    for imageFormat, image in firstGlyphWithStrikes.imgDict.items():
        if imageFormat.split('-')[0] == "png":
            cblc.append(strike(metrics, strikeIndex, image.strike, glyphs))
            strikeIndex += 1




    return cblc

from lxml.etree import Element
from tables.support.eblc_ebdt import SmallGlyphMetrics, BigGlyphMetrics



def format17(metrics, strikeIndex, strikeRes, subfolder, glyphs):
    """
    Generates data for a single bitmap according to EBLC/CBLC subtable format 17.
    This is actually the only working subtable format in TTX.

    Way to go TTX.
    """

    # start of strikes
    # (which we're fudging right now)
    # ------------------------------------------------------------
    strike = Element("strikedata", {"index": str(strikeIndex)})

    for g in glyphs['img']:

        # you only put them in if there's an actual image
        if g.img:

            # format 18 for big metrics and PNG data.
            bitmapTable = Element("cbdt_bitmap_format_17", {"name": g.codepoints.name() })

            bitmapTable.append(SmallGlyphMetrics(metrics))

            rawImageData = Element("rawimagedata")
            rawImageData.text = g.img[subfolder].getHexDump()

            bitmapTable.append(rawImageData)

            strike.append(bitmapTable)

    return strike


def format18(metrics, strikeIndex, strikeRes, subfolder, glyphs):
    """
    Generates data for a single bitmap according to EBLC/CBLC subtable format 18.
    This isn't actually supported in TTX but I'm making this in case it ever is supported.

    Way to go TTX.
    """


    # start of strikes
    # (which we're fudging right now)
    # ------------------------------------------------------------
    strike = Element("strikedata", {"index": str(strikeIndex)})

    for g in glyphs['img']:

        # you only put them in if there's an actual image
        if g.img:

            # format 18 for big metrics and PNG data.
            bitmapTable = Element("cbdt_bitmap_format_18", {"name": g.codepoints.name() })


            bitmapTable.append(BigGlyphMetrics(metrics))

            rawImageData = Element("rawimagedata")
            rawImageData.text = g.img[subfolder].getHexDump()

            bitmapTable.append(rawImageData)

            strike.append(bitmapTable)

    return strike



def format19(strikeIndex, strikeRes, subfolder, glyphs):
    """
    Generates data for a single bitmap according to EBLC/CBLC subtable format 19.
    This isn't actually supported in TTX but I'm making this in case it ever is supported.

    Way to go TTX.
    """

    # start of strikes
    # (which we're fudging right now)
    # ------------------------------------------------------------
    strike = Element("strikedata", {"index": str(strikeIndex)})

    for g in glyphs['img']:

        # you only put them in if there's an actual image
        if g.img:

            # format 18 for big metrics and PNG data.
            bitmapTable = Element("cbdt_bitmap_format_19", {"name": g.codepoints.name() })

            rawImageData = Element("rawimagedata")
            rawImageData.text = g.img[subfolder].getHexDump()

            bitmapTable.append(rawImageData)

            strike.append(bitmapTable)

    return strike




def create(m, glyphs):
    """
    Generates and returns a glyf table with dummy data.
    """

    metrics = m['metrics']

    cbdt = Element("CBDT")

    cbdt.append(Element("header", {"version": "3.0"})) # hard-coded



    # get basic strike information.

    for g in glyphs['img']:
        if g.img:
            firstGlyphWithStrikes = g
            break


    # iterate over each strike.

    strikeIndex = 0

    for imageFormat, image in firstGlyphWithStrikes.img.items():
        if imageFormat.split('-')[0] == "png":
            cbdt.append(format17(metrics, strikeIndex, image.strike, imageFormat, glyphs))
            strikeIndex += 1



    return cbdt

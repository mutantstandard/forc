import xml.etree.ElementTree as ET

def svg(glyphs):
    """
    Generates and returns a SVG table.
    """

    svgTable = ET.Element("SVG")

    for ID, g in enumerate(glyphs):
        if g.imagePath:
            svgElement = ET.Element("svgDoc", {"startGlyph": str(ID), "endGlyph" : str(ID) })
            svgTable.append(svgElement)

            svgImage = ET.parse(g.imagePath)




    #
    #   - check if the SVG has an attribute called 'viewbox'
    #
    #   - if it does, remove it, and add a group inside
    #     applying the right transform, based on:
    #
    #        - PPEM
    #        - ascender, descender, bounding box
    #
    # stuff the edited SVG into CDATA.
    #


    return svgTable

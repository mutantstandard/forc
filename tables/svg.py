from xml.etree.ElementTree import Element

def svg():
    """
    Generates and returns a SVG table.
    """
    svgTable = Element("SVG")

    # here you will need to add all of the juicy glyphs.
    # for each blah blah
    #   svgElement = Element("svgDoc", {"startGlyph": ID, "endGlyph" : ID})
    #   - check if the SVG has an attribute called 'viewbox'
    #   - if it does, remove it, and add a group inside applying the right transform, based on:
    #        - PPEM
    #        - ascender, descender, bounding box
    # stuff the edited SVG into CDATA.


    return svgTable

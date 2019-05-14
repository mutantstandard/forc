import lxml.etree as etree

from io import BytesIO
from transform.svg import stripStyles, affinityDesignerCompensate, viewboxCompensate




def TTXaddGlyphID(svgImage, ID):
    """
    Adds the glyph ID to the SVG.
    """

    svg = svgImage.getroot()


    svg.attrib["id"] = f"glyph{ID}"
    newSVGTree = svg.getroottree()

    return newSVGTree




def toTTX(m, glyphs, afsc):
    """
    Generates and returns a SVG table.

    It will non-destructively alter glyphs or throw exceptions if there's visual data
    that's incompatible with SVGinOT standards and/or renderers.
    """

    metrics = m['metrics']

    svgTable = etree.Element("SVG")

    for ID, g in enumerate(glyphs["img_empty"]):

        if g.img:
            finishedSVG = TTXaddGlyphID(g.img['svg'].data, ID)

            svgDoc = etree.Element("svgDoc", {"startGlyphID": str(ID), "endGlyphID" : str(ID) })
            cdata = etree.CDATA(etree.tostring(finishedSVG, method="xml", pretty_print=False, xml_declaration=True, encoding="UTF-8"))

            svgDoc.text = cdata
            svgTable.append(svgDoc)



    return svgTable

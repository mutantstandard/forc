import lxml.etree as etree

from io import BytesIO
from transform.svg import stripStyles, affinityDesignerCompensate, viewboxCompensate




def addGlyphID(svgTree, ID):
    """
    Adds the glyph ID to the SVG.
    """
    svg = svgTree.getroot()


    svg.attrib["id"] = f"glyph{ID}"
    newSVGTree = svg.getroottree()

    return newSVGTree




def create(m, glyphs, afsc):
    """
    Generates and returns a SVG table.

    It will non-destructively alter glyphs or throw exceptions if there's visual data
    that's incompatible with SVGinOT standards and/or renderers.
    """

    metrics = m['metrics']

    svgTable = etree.Element("SVG")

    for ID, g in enumerate(glyphs['img']):
        if g.imagePath and g.imagePath['svg']:
            svgDoc = etree.Element("svgDoc", {"startGlyphID": str(ID), "endGlyphID" : str(ID) })

            # lxml can't parse from Path objects, so it has to give a string representation.
            svgImage = etree.parse(g.imagePath['svg'].path.as_uri())


            cdata = etree.CDATA("")

            # strip styles if there are any.
            if svgImage.find(f"//*[@style]") is not None:
                stripStyles(svgImage)

            if afsc:
                affinityDesignerCompensate(svgImage)

            finishedSVG = etree.ElementTree(etree.Element("svg"))

            # check if there's a viewBox and compensate for it if that's the case.
            # if not, just pass it on.
            # -------------------------------------------------------------------------------------
            if svgImage.find(".[@viewBox]") is not None:
                compensated = viewboxCompensate(metrics, svgImage, ID)
                finishedSVG = addGlyphID(compensated, ID)

            else:
                finishedSVG = addGlyphID(svgImage, ID)


            cdata = etree.CDATA(etree.tostring(finishedSVG, method="xml", pretty_print=False, xml_declaration=True, encoding="UTF-8"))

            svgDoc.text = cdata
            svgTable.append(svgDoc)





    return svgTable

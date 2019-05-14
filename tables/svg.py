import lxml.etree as etree

from io import BytesIO
from transform.svg import stripStyles, affinityDesignerCompensate, viewboxCompensate



class svgDoc:
    """
    Class representing an SVG document in an SVG table.
    """

    def __init__(self, glyphID, glyph):
        self.img = glyph.imgDict['svg']
        self.ID = glyphID

    def toTTX(self):
        # create the structure that encapsulates the SVG image
        svgDoc = etree.Element("svgDoc", {"startGlyphID": str(self.ID), "endGlyphID" : str(self.ID) })

        # Add a glyph ID to the SVG.
        svgRoot = self.img.data.getroot()
        svgRoot.attrib["id"] = f"glyph{self.ID}"
        newSVGTree = svgRoot.getroottree()
        finishedSVG = newSVGTree


        cdata = etree.CDATA(etree.tostring(finishedSVG, method="xml", pretty_print=False, xml_declaration=True, encoding="UTF-8"))
        svgDoc.text = cdata

        return svgDoc


class svg:
    """
    Class representing an SVG table.
    """

    def __init__(self, m, glyphs):

        self.graphics = []

        for ID, g in enumerate(glyphs["img_empty"]):  # it has to be img_empty because we need those glyph indexes.
            if g.imgDict:
                self.graphics.append(svgDoc(ID, g))


    def toTTX(self):

        svgTable = etree.Element("SVG")

        for svgDoc in self.graphics:
            svgTable.append(svgDoc.toTTX())

        return svgTable

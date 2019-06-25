import struct
import lxml.etree as etree

from io import BytesIO
from transform.svg import stripStyles, affinityDesignerCompensate, viewboxCompensate



class SVGDoc:
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


class SVG:
    """
    Class representing an SVG table.
    """

    def __init__(self, m, glyphs):

        self.tableName = "SVG" # hard-coded. For font generation only.

        self.version = 0 # hardcoded; the only version.
        self.SVGDocumentList = []
        self.reserved = 0 # reserved; set to 0.

        for ID, g in enumerate(glyphs["img_empty"]):  # it has to be img_empty because we need those glyph indexes.
            if g.imgDict:
                self.SVGDocumentList.append(SVGDoc(ID, g))


    def toTTX(self):
        svgTable = etree.Element("SVG")
        # - TTX doesnt have version for SVG table.
        for svgDoc in self.SVGDocumentList:
            svgTable.append(svgDoc.toTTX())

        return svgTable


    def toBytes(self):
        # TODO: compile and attach SVGDocumentList.
        # - compile and calculate Offset32 to SVGDocumentList here
        svg = struct.pack( ">HI"
                         , self.version # UInt16
                         # - offsetToSVGDocumentList # Offset32/UInt32
                         , self.reserved # UInt32
                         )

        # Attach SVGDocumentList afterwards.

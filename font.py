from lxml.etree import Element, tostring

import log
from format import formats

import tables.glyphOrder
import tables.head
import tables.os2
import tables.post
import tables.name
import tables.maxp
import tables.gasp
import tables.loca
import tables.dsig

import tables.hhea
import tables.hmtx
import tables.vhea
import tables.vmtx

import tables.cmap
# import tables.gdef
# import tables.gpos
import tables.gsub
# import tables.morx

import tables.glyf
import tables.svg
import tables.sbix
import tables.cbdt
import tables.cblc




class font:
    def __init__(self, chosenFormat, m, glyphs, flags):
        """
        Covers the entire routine for assembling a TTX file.
        """

        glyphFormat = formats[chosenFormat]["imageTables"]


        self.tables = []

        # COLOR CODES:
        # 90 (gray):        a standard table that gets compiled no matter what.
        # 36 (dark cyan):   a table that is only compiled based on the font format.


        # headers and other weird crap
        # ---------------------------------------------
        log.out('[glyphOrder] ', 90, newline=False)
        self.tables.append(tables.glyphOrder.glyphOrder(glyphs))

        log.out('[head] ', 90, newline=False)
        self.tables.append(tables.head.head(m))

        log.out('[OS/2] ', 90, newline=False)
        self.tables.append(tables.os2.os2(m, glyphs))

        log.out('[post] ', 90, newline=False)
        self.tables.append(tables.post.post(glyphs))

        # maxp is a semi-placeholder table.
        log.out('[maxp] ', 90, newline=False)
        self.tables.append(tables.maxp.maxp(glyphs))

        log.out('[gasp] ', 90, newline=False)
        self.tables.append(tables.gasp.gasp())




        # loca is a placeholder to make macOS happy.
        #
        # CBDT/CBLC either doesn't use loca or TTX doesn't want
        # an empty loca table if there's no gly table (CBDT/CBLC
        # fonts shouldnt have glyf tables.)

        if glyphFormat is not "CBx":
            log.out('[loca] ', 36, newline=False)
            self.tables.append(tables.loca.loca())

        # placeholder table that makes Google's font validation happy.
        log.out('[DSIG]', 90)
        self.tables.append(tables.dsig.dsig())






        # horizontal and vertical metrics tables
        # ---------------------------------------------
        log.out('[hhea] ', 90, newline=False)
        self.tables.append(tables.hhea.hhea(m))

        log.out('[hmtx] ', 90, newline=False)
        self.tables.append(tables.hmtx.hmtx(m, glyphs))

        log.out('[vhea] ', 90, newline=False)
        self.tables.append(tables.vhea.vhea(m))

        log.out('[vmtx]', 90)
        self.tables.append(tables.vmtx.vmtx(m, glyphs))




        # glyph-code mappings
        # ---------------------------------------------

        # single glyphs
        log.out('[cmap] ', 90, newline=False)
        self.tables.append(tables.cmap.cmap(glyphs, flags["no_vs16"]))



        # ligatures
        ligatures = False

        # check for presence of ligatures
        for g in glyphs:
            if len(g) > 1:
                ligatures = True

        if ligatures:

            if formats[chosenFormat]["ligatureFormat"] == "OpenType":
                log.out('[GSUB] ', 36, newline=False)
                self.tables.append(tables.gsub.gsub(glyphs))



        # glyf
        # ---------------------------------------------

        # glyf is used as a placeholde to please font validation,
        # table dependencies and the TTX compiler.
        #
        # CBDT/CBLC doesn't use glyf at all
        if glyphFormat is not "CBx":
            log.out('[glyf] ', 36, newline=False)
            self.tables.append(tables.glyf.glyf(m, glyphs))


        # actual glyph picture data
        # ---------------------------------------------

        if glyphFormat == "SVG":
            log.out('[SVG ]', 36)
            self.tables.append(tables.svg.svg(m, glyphs))

        elif glyphFormat == "sbix":
            log.out('[sbix]', 36)
            self.tables.append(tables.sbix.sbix(glyphs))

        elif glyphFormat == "CBx":
            log.out('[CBLC] ', 36, newline=False)
            self.tables.append(tables.cblc.cblc(m, glyphs))

            log.out('[CBDT]', 36)
            self.tables.append(tables.cbdt.cbdt(m, glyphs))




        # human-readable metadata
        # ---------------------------------------------
        log.out('[name]', 90)
        self.tables.append(tables.name.name(chosenFormat, m))


    def toTTX(self, asString=False):
        """
        Compiles font to TTX.
        """

        # start the TTX file
        # ---------------------------------------------
        root = Element('ttFont', {'sfntVersion': '\\x00\\x01\\x00\\x00', 'ttLibVersion': '3.28'}) # hard-coded attrs.

        # get all of this font's tables' TTX representations and append them to the file.
        for t in self.tables:
            root.append(t.toTTX())


        # the TTX is now done! (as long as something didn't go wrong)
        # choose whether to get the result as a formatted string or as an lxml Element.
        if asString:
            return tostring(root, pretty_print=True, method="xml", xml_declaration=True, encoding="UTF-8")
        else:
            return root


    def toBytes(self):
        """
        Compiles font to bytes.
        (Just a placeholder right now.)
        """

        ## create a valid font header

        ## build first time + put together

        ## make a checksum for it

        ## edit head.checkSumAdjustment to have this checksum

        ## build + put together one last time and return that.

        return "0"

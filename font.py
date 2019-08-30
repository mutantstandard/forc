from lxml.etree import Element, tostring
from math import log2, floor
from transform.bytes import calculateTableChecksum, generateOffsets
import struct

import log
from format import formats
from data import Tag

import tables.tableRecord

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




class TTFont:
    """
    Class representing a TrueType/OpenType font.
    """


    def __init__(self, chosenFormat, m, glyphs, flags):
        """
        Covers the entire routine for assembling a TrueType/OpenType font with forc input data.
        """

        glyphFormat = formats[chosenFormat]["imageTables"]


        self.tables = {}


        try:
            # not actually tables
            # ---------------------------------------------
            self.glyphOrder = tables.glyphOrder.GlyphOrder(glyphs)



            # headers and other weird crap
            # ---------------------------------------------
            log.out('[head] ', 90, newline=False)
            self.tables["head"] = tables.head.head(m)

            log.out('[OS/2] ', 90, newline=False)
            self.tables["OS/2"] = tables.os2.OS2(m, glyphs)

            #log.out('[post] ', 90, newline=False)
            #self.tables.append(tables.post.post(glyphs))

            # maxp is a semi-placeholder table.
            log.out('[maxp] ', 90, newline=False)
            self.tables["maxp"] = tables.maxp.maxp(glyphs)

            log.out('[gasp] ', 90, newline=False)
            self.tables["gasp"] = tables.gasp.gasp()




            # loca is a placeholder to make macOS happy.
            #
            # CBDT/CBLC either doesn't use loca or TTX doesn't want
            # an empty loca table if there's no glyf table (CBDT/CBLC
            # fonts shouldnt have glyf tables.)

            if glyphFormat is not "CBx":
                log.out('[loca] ', 36, newline=False)
                self.tables["loca"] = tables.loca.loca()

            # placeholder table that makes Google's font validation happy.
            log.out('[DSIG]', 90)
            self.tables["DSIG"] = tables.dsig.DSIG()






            # horizontal and vertical metrics tables
            # ---------------------------------------------
            log.out('[hhea] ', 90, newline=False)
            self.tables["hhea"] = tables.hhea.hhea(m)

            log.out('[hmtx] ', 90, newline=False)
            self.tables["hmtx"] = tables.hmtx.hmtx(m, glyphs)

            log.out('[vhea] ', 90, newline=False)
            self.tables["vhea"] = tables.vhea.vhea(m)

            log.out('[vmtx]', 90)
            self.tables["vmtx"] = tables.vmtx.vmtx(m, glyphs)




            # glyph-code mappings
            # ---------------------------------------------

            # single glyphs
            log.out('[cmap] ', 90, newline=False)
            self.tables["cmap"] = tables.cmap.cmap(glyphs, flags["no_vs16"])



            # ligatures
            ligatures = False

            # check for presence of ligatures
            for g in glyphs:
                if len(g) > 1:
                    ligatures = True

            if ligatures:

                if formats[chosenFormat]["ligatureFormat"] == "OpenType":
                    log.out('[GSUB] ', 36, newline=False)
                    self.tables["GSUB"] = tables.gsub.GSUB(glyphs)



            # glyf
            # ---------------------------------------------

            # glyf is used as a placeholde to please font validation,
            # table dependencies and the TTX compiler.
            #
            # CBDT/CBLC doesn't use glyf at all
            if glyphFormat is not "CBx":
                log.out('[glyf] ', 36, newline=False)
                self.tables["glyf"] = tables.glyf.glyf(m, glyphs)


            # actual glyph picture data
            # ---------------------------------------------

            if glyphFormat == "SVG":
                log.out('[SVG ]', 36)
                self.tables["SVG "] = tables.svg.SVG(m, glyphs)

            elif glyphFormat == "sbix":
                log.out('[sbix]', 36)
                self.tables["sbix"] = tables.sbix.sbix(glyphs)

            elif glyphFormat == "CBx":
                log.out('[CBLC] ', 36, newline=False)
                self.tables["CBLC"] = tables.cblc.CBLC(m, glyphs)

                log.out('[CBDT]', 36)
                self.tables["CBDT"] = tables.cbdt.CBDT(m, glyphs)




            # human-readable metadata
            # ---------------------------------------------
            log.out('[name]', 90)
            self.tables["name"] = tables.name.name(chosenFormat, m)

        except ValueError as e:
            ValueError(f"Something went wrong with building the font class. -> {e}")





    def test(self):
        """
        A series of tests determining the validity of the font, checking certain
        variables between font tables that must agree with each other (as opposed to
        checking issues that exist solely within a certain table).
        """



        # certain bits in head.macStyle and OS/2.fsSelection must agree with each other.
        # ------------------------------------------------------------------------------
        macStyleBold = self.tables["head"].macStyle.toList()[0]
        fsSelectionBold = self.tables["OS/2"].fsSelection.toList()[5]
        macStyleItalic = self.tables["head"].macStyle.toList()[1]
        fsSelectionItalic = self.tables["OS/2"].fsSelection.toList()[0]

        if macStyleBold != fsSelectionBold:
            log.out(f"💢 The Bold bit in head.macStyle (bit 0: {macStyleBold}) does not agree with OS/2.fsSelection (bit 5: {fsSelectionBold})", 91)

        if macStyleItalic != fsSelectionItalic:
            log.out(f"💢 The Italic bit in head.macStyle (bit 1: {macStyleItalic}) does not agree with OS/2.fsSelection (bit 0: {fsSelectionItalic})", 91)


        # number of glyphs in an sbix strike must be equal to maxp.numGlyphs.
        # ------------------------------------------------------------------------------
        maxpNumGlyphs = self.tables["maxp"].numGlyphs
        if "sbix" in self.tables:
            strikes = self.tables["sbix"].strikes
            for num, s in enumerate(strikes):
                if len(s.bitmaps) != self.tables["maxp"].numGlyphs:
                    log.out(f"💢 the number of bitmaps inside sbix strike index {num} (ppem: {s.ppem}, ppi: {s.ppi}) doesn't match maxp.numGlyphs. (sbix strike: {len(s.bitmaps)}, maxp.numGlyphs: {self.tables['maxp'].numGlyphs}).", 91)







    def toTTX(self, asString=False):
        """
        Compiles font class to a TTX-formatted string.
        """

        # start the TTX file
        # ---------------------------------------------
        root = Element('ttFont', {'sfntVersion': '\\x00\\x01\\x00\\x00', 'ttLibVersion': '3.28'}) # hard-coded attrs.

        # get all of this font's tables' TTX representations and append them to the file.
        root.append(self.glyphOrder.toTTX())

        for tableName, t in self.tables.items():
            root.append(t.toTTX())


        # the TTX is now done! (as long as something didn't go wrong)
        # choose whether to get the result as a formatted string or as an lxml Element.
        if asString:
            return tostring(root, pretty_print=True, method="xml", xml_declaration=True, encoding="UTF-8")
        else:
            return root



    def bytesPass(self):
        """
        Represents a single compile pass to bytes.
        (Just a WIP/placeholder right now.)
        """

        # offset table (ie. the font header)
        # --------------------------------------------------------------
        # (this should be fine and complete)

        numTables = len(self.tables)
        searchRange = (2 ** floor(log2(numTables))) * 16
        entrySelector = int(log2(floor(log2(numTables))))
        rangeShift = numTables * 16 - searchRange

        offsetTable = struct.pack( ">IHHHH"
                                 , 0x00010000 # sfntVersion, UInt32
                                 , numTables # UInt16
                                 , searchRange # UInt16
                                 , entrySelector # UInt16
                                 , rangeShift # UInt16
                                 )


        # table record entries
        # -------------------------------------------------------------

        initialTables = []
        originalLengths = []
        checkSums = []
        tags = []

        # get all of the table data
        for tableName, t in self.tables.items():
            #print(f"converting {tableName} to bytes...")

            # convert to bytes
            try:
                tableOutput = t.toBytes()
            except ValueError as e:
                raise ValueError(f"Something has gone wrong with converting the {tableName} table to bytes. -> {e}")

            initialTables.append(tableOutput[0])
            originalLengths.append(tableOutput[1])

            # get a checksum on that data
            try:
                checkSums.append(calculateTableChecksum(tableOutput[0]))
            except ValueError as e:
                raise ValueError(f"Something has gone wrong with calculating the checksum for {tableName}. -> {e}")

            # also add a tag.
            tags.append(tableName)


        # calculate offsets for each table
        initialOffset = (len(self.tables) * 16) + 12 # 16 = tableRecord length, 12 = offset table length.
        tableOffsets = generateOffsets(initialTables, 32, initialOffset, usingClasses=False)

        tableRecordsList = []

        for n, t in enumerate(initialTables):
                tableRecordsList.append(tables.tableRecord.TableRecord( tags[n]
                                               , checkSums[n]
                                               , tableOffsets["offsetInts"][n]
                                               , originalLengths[n]
                                               ))
        #print(tableRecordsList)

        tableRecordsList.sort()
        tableRecords = b''

        for t in tableRecordsList:
            tableRecords += t.toBytes()

        return offsetTable + tableRecords + tableOffsets["bytes"]



    def toBytes(self):
        """
        Compiles font class to bytes, including checksum.
        (Just a placeholder right now.)
        """

        log.out('first compilation pass...', 90)
        firstPass = self.bytesPass()

        log.out('calculating checksum...', 90)
        initialCS = calculateTableChecksum(firstPass)
        checkSumAdjustment = (0xB1B0AFBA - initialCS) % 0x100000000
        self.tables["head"].checkSumAdjustment = checkSumAdjustment

        log.out('last compilation pass...', 90)
        lastPass = self.bytesPass()


        return lastPass

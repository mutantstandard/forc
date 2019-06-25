from lxml.etree import Element, tostring
from math import log2, floor
from transform.bytes import calculateChecksum, generateOffsets
import struct

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




class TTFont:
    """
    Class representing a TrueType/OpenType font.
    """


    def __init__(self, chosenFormat, m, glyphs, flags):
        """
        Covers the entire routine for assembling a TrueType/OpenType font with forc input data.
        """

        glyphFormat = formats[chosenFormat]["imageTables"]


        self.tables = []


        try:
            # headers and other weird crap
            # ---------------------------------------------
            self.glyphOrder = tables.glyphOrder.GlyphOrder(glyphs)



            log.out('[head] ', 90, newline=False)
            self.tables.append(tables.head.head(m))

            log.out('[OS/2] ', 90, newline=False)
            self.tables.append(tables.os2.OS2(m, glyphs))

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
            self.tables.append(tables.dsig.DSIG())






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
                    self.tables.append(tables.gsub.GSUB(glyphs))



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
                self.tables.append(tables.svg.SVG(m, glyphs))

            elif glyphFormat == "sbix":
                log.out('[sbix]', 36)
                self.tables.append(tables.sbix.sbix(glyphs))

            elif glyphFormat == "CBx":
                log.out('[CBLC] ', 36, newline=False)
                self.tables.append(tables.cblc.CBLC(m, glyphs))

                log.out('[CBDT]', 36)
                self.tables.append(tables.cbdt.CBDT(m, glyphs))




            # human-readable metadata
            # ---------------------------------------------
            log.out('[name]', 90)
            self.tables.append(tables.name.name(chosenFormat, m))

        except ValueError as e:
            ValueError(f"Something went wrong with building the font class. -> {e}")




    def toTTX(self, asString=False):
        """
        Compiles font class to a TTX-formatted string.
        """

        # start the TTX file
        # ---------------------------------------------
        root = Element('ttFont', {'sfntVersion': '\\x00\\x01\\x00\\x00', 'ttLibVersion': '3.28'}) # hard-coded attrs.

        # get all of this font's tables' TTX representations and append them to the file.
        root.append(self.glyphOrder.toTTX())

        for t in self.tables:
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
        # - sorted in ascending order by tag (first to last letters/numbers)
        # - offsets are measured from the very beginning of the font file.
        #   -12 bytes,

        initialTables = []
        checkSums = []
        tags = []

        for t in self.tables:
            data = t.toBytes()
            print(t.tableName)
            initialTables.append(data)
            checkSums.append(calculateChecksum(data))
            tags.append(t.tableName)

        offsetPos = (len(self.tables) * -16) - 12 # 16 = tableRecord, 12 = offset table.
        tableOffsets = generateOffsets(initialTables, 32, offsetPos)

        tableRecordsList = []

        for n, t in initialtables.items():
                tableRecords.append(tableRecord( tags[n]
                                               , checkSums[n]
                                               , tableOffsets["offsets"][n]
                                               , checkSums[n]
                                               , len(initialTables[n])
                                               ))

        tableRecordsList.sort()
        tableRecords = bytes()
        # TODO: convert tableRecords into bytes.

        return offsetTable + tableRecords + tableOffsets["bytes"]



    def toBytes(self):
        """
        Compiles font class to bytes, including checksum.
        (Just a placeholder right now.)
        """
        log.out('building the first time...', 90)

        ## build first time + put together
        # header.append(bytesPass(self))

        log.out('calculating checksum...', 90)

        ## make a checksum for it
        # self.head.checkSumAdjustment = ???

        log.out('final pass...', 90)
        ## one last conversion to bytes.
        # return bytesPass(self)

        return self.bytesPass()

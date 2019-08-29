import struct
from lxml.etree import Element
from tables.common.cmapSubtables import cmapFormat0, cmapFormat4, cmapFormat12, cmapFormat14
from transform.bytes import generateOffsets, outputTableBytes


class cmap:
    """
    Class representing a cmap table.
    """

    def __init__(self, glyphs, no_vs16):

        self.version = 0 # hardcoded. no other version.

        # check what's what in this set to determine what subtables to toTTX.
        # ---------------------------------------------------------
        oneByte = []
        twoByte = []
        fourByte = []
        vs = []

        for g in glyphs['all']:
            if no_vs16 is False and g.codepoints.vs16:
                vs.append(g)

            if len(g) == 1:
                if g.codepoints.seq[0] <= int('ff', 16):
                    oneByte.append(g)
                if g.codepoints.seq[0] <= int('ffff', 16):
                    twoByte.append(g)
                if g.codepoints.seq[0] <= int('ffffff', 16):
                    fourByte.append(g)


        self.subtables = []

        if oneByte:
            self.subtables.append(cmapFormat0(oneByte, platformID=1, platEncID=0, language=0))

        if twoByte:
             # platform ID 0 (Unicode)
            self.subtables.append(cmapFormat4(twoByte, platformID=0, platEncID=3, language=0))

            # platform ID 3 (Microsoft)
            # platEncID should be 1. This is what is required to make
            # this particular cmap subtable format work.
            self.subtables.append(cmapFormat4(twoByte, platformID=3, platEncID=1, language=0))

        if fourByte:
            # platform ID 0 (Unicode)
            self.subtables.append(cmapFormat12(fourByte, platformID=0, platEncID=10, language=0))

            # platform ID 3 (Microsoft)
            # platEncID should be 10. This is what is required to make
            # this particular cmap subtable format work.
            self.subtables.append(cmapFormat12(fourByte, platformID=3, platEncID=10, language=0))

        if vs:
            self.subtables.append(cmapFormat14(vs, platformID=0, platEncID=5))



    def toTTX(self):
        cmap = Element("cmap")

        # - TTX doesnt have version for cmap table.
        cmap.append(Element("tableVersion", {"version": str(self.version)}))

        for sub in self.subtables:
            cmap.append(sub.toTTX())

        return cmap



    def toBytes(self):

        # initialise some stuff
        subtableOffsets = generateOffsets(self.subtables, 32, 4 + (8 * len(self.subtables))) ## placheholder. last one should be (8 * len(self.subtables)
        encodingRecords = b''


        # prepare the chunks
        header = struct.pack( ">HH"
                          , self.version # UInt16
                          , len(self.subtables) # UInt16
                          )

        for num, subtable in enumerate(self.subtables):
            encodingEntry = struct.pack( ">HHI"
                       , subtable.platformID # UInt16
                       , subtable.platEncID # UInt16
                       , subtableOffsets["offsetInts"][num] # Offset32 (UInt32
                       )
            encodingRecords += encodingEntry


        return outputTableBytes(header + encodingRecords + subtableOffsets["bytes"])

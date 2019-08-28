import struct
import array
from lxml.etree import Element
from math import floor, log2

def makeTTXSubtable(tag, attrs, cmapGlyphSet):
    subtable = Element(tag, attrs)

    for g in cmapGlyphSet:
        if not g.alias:
            subtable.append(Element("map", {"code": hex(g.codepoints.seq[0]), "name": g.name() }))
        else:
            subtable.append(Element("map", {"code": hex(g.codepoints.seq[0]), "name": g.alias.name() }))
    return subtable

def makeGlyphIDArray(glyphs):
    """
    makes a glyph
    """
    pass

class cmapFormat0:
    """
    Class representing cmap subtable format 0.
    (Subtable representing codepoints from U+0 - U+FF.)

    - https://docs.microsoft.com/en-us/typography/opentype/spec/cmap#format-0-byte-encoding-table
    """

    def __init__(self, glyphs, platformID, platEncID, language):

        # check if the glyphs are one-byte, reject them if they are not.
        for g in glyphs:
            if g.codepoints.seq[0] > int('ff', 16):
                raise ValueError(f"Creating cmap subtable format 0 has been rejected. A glyph whose codepoint is greater than U+FF was given. cmap Subtable Format 0 must have codepoints less than or equal to U+FF.")

        self.format = 0 # hardcoded
        self.platformID = platformID
        self.platEncID = platEncID
        self.language = language
        self.glyphs = glyphs

    def toTTX(self):
        return makeTTXSubtable(  "cmap_format_0",
                                { "platformID": str(self.platformID)
                                , "platEncID": str(self.platEncID)
                                , "language": str(self.language)
                                }
                                , self.glyphs
                                )

    def toBytes(self):
        beginning = struct.pack( ">HHH"
                          , self.format # UInt16

                          # length (in bytes) of the subtable. (it's a static length!)
                          , 262 #UInt16

                          , self.language # UInt16
                          )

        # initialise list with a fixed size
        glyphIdArray = [0x00] * 256 # MAYBE: I presume that no value is 0x00.

        for id, glyph in enumerate(self.glyphs):
            glyphIdArray[id] = glyph.codepoints.seq[0]

        return beginning + array.array('B', glyphIdArray)



class cmapFormat4:
    """
    Class representing cmap subtable format 4.
    (Subtable representing codepoints from U+0 - U+FFFF.)

    - https://docs.microsoft.com/en-us/typography/opentype/spec/cmap#format-4-segment-mapping-to-delta-values
    """

    def __init__(self, glyphs, platformID, platEncID, language):

        # check if the glyphs are two-byte, reject them if they are not.
        for g in glyphs:
            if g.codepoints.seq[0] > int('ffff', 16):
                raise ValueError(f"Creating cmap subtable format 4 has been rejected. A glyph whose codepoint is greater than U+FFFF was given. cmap Subtable Format 4 must only have codepoints less than or equal to U+FFFF.")

        self.format = 4 # hard-coded.
        self.glyphs = glyphs
        self.platformID = platformID
        self.platEncID = platEncID
        self.language = language


    def toTTX(self):
        return makeTTXSubtable(  "cmap_format_4",
                                { "platformID": str(self.platformID)
                                , "platEncID": str(self.platEncID)
                                , "language": str(self.language)
                                }
                                , self.glyphs
                                )

    def toBytes(self):

        reservedPad = 0 # hardcoded

        endCode = []
        startCode = []
        idDelta = []
        idRangeOffset = []
        segCount = 0

        # generate segments
        for id, glyph in enumerate(self.glyphs):
            thisGlyphCodepoint = glyph.codepoints.seq[0]
            lastGlyphCodepoint = self.glyphs[id-1].codepoints.seq[0]

            if id == 0:
                segCount +=1
                startCode.append(thisGlyphCodepoint)
            else:
                # check if it's continuous with the last glyph.
                if thisGlyphCodepoint != (lastGlyphCodepoint + 1):
                    endCode.append(lastGlyphCodepoint)
                    startCode = thisGlyphCodepoint
                    segCount += 1
                else:
                    pass

        # TODO: learn how to calculate idDelta and idRangeOffset
        # TODO: add terminating entries to these arrays.

        # METADATA
        # Generate a bunch of metadata. these calculations are what they are (and they're tested to be correct).
        segCountX2 = segCount * 2
        searchRange = 2 * (2 ** floor(log2(39)))
        entrySelector = floor(log2(searchRange / 2))
        rangeShift = 2 * segCount - searchRange
        rangeShift = max(rangeShift, 0)



        # RANGES AND OTHER STUFF
        reservedPad = 0 # hard-coded

        startCode = []
        endCode = []
        idDelta = []

        currentDelta = 0 # just for the upcoming loop

        for g in range(0, len(self.glyphs)):
            if g == 0:
                startCode.append(self.glyphs[g].codepoints.seq[0])
            else:
                if self.glyphs[g].codepoints.seq[0] == self.glyphs[g-1].codepoints.seq[0] + 1:
                    currentDelta += 1
                else:
                    endCode.append(self.glyphs[g-1].codepoints.seq[0])
                    idDelta.append(-currentDelta) # deltas in this should be negative
                    currentDelta = 0


        beginning = struct.pack( ">HHHHHH"
                          , self.format # UInt16
                          # length # UInt16
                          , self.language # UInt16
                          , segCountX2 # UInt16
                          , searchRange # UInt16
                          , entrySelector # UInt16
                          , rangeShift # UInt16
                          )


        # beginning + startCode + endCode + reservedPad + idDelta


        # TODO: create bytes representations of these and compile.
              # idRangeOffset[segCount] # UInt16. Offsets into glyphIdArray or 0.
              # glyphIdArray[] # Array of UInt16s.

        return b'' # placeholder



class SequentialMapGroupRecord:
    """
    Class representing a SequentialMapGroup Record in a cmap Subtable Format 12.

    This is only used during bytes compilation.
    """
    def __init__ (self, startCharCode, endCharCode, startGlyphID):
        self.startCharCode = startCharCode
        self.endCharCode = endCharCode
        self.startGlyphID = startGlyphID

    def toBytes(self):
        return struct.pack(">III"
                    , self.startCharCode
                    , self.endCharCode
                    , self.startGlyphID)


class cmapFormat12:
    """
    Class representing cmap subtable format 12.
    (Subtable representing codepoints from U+0 - U+FFFFFF.)

    - https://docs.microsoft.com/en-us/typography/opentype/spec/cmap#format-12-segmented-coverage
    """

    def __init__(self, glyphs, platformID, platEncID, language):

        # check if the glyphs are four-byte, reject them if they are not.
        for g in glyphs:
            if g.codepoints.seq[0] > int('ffffff', 16):
                raise ValueError(f"Creating cmap subtable format 12 has been rejected. A glyph whose codepoint is greater than U+FFFFFF was given. cmap Subtable Format 12 must only have codepoints less than or equal to U+FFFFFF.")

        self.format = 12 # hard-coded.
        self.glyphs = glyphs
        self.platformID = platformID
        self.platEncID = platEncID
        self.language = language


    def toTTX(self):
        return makeTTXSubtable(  "cmap_format_12",
                                { "platformID": str(self.platformID)
                                , "platEncID": str(self.platEncID)
                                , "language": str(self.language)
                                , "format": "12"
                                , "reserved": "0"
                                , "length": "0"
                                , "nGroups": "0"
                                }
                                , self.glyphs
                                )
    def toBytes(self):

        startCode = 0
        endCode = 0
        startCodeID = 0
        sequentialMapGroup = []

        for g in range(0, len(self.glyphs)):
            if g == 0:
                startCode = self.glyphs[g].codepoints.seq[0]
                startCodeID = g
            else:
                if self.glyphs[g].codepoints.seq[0] != self.glyphs[g-1].codepoints.seq[0] + 1:
                    endCode = self.glyphs[g-1].codepoints.seq[0]
                    sequentialMapGroup.append(SequentialMapGroupRecord(startCode, endCode, startCodeID))

        subtableLength = 16 + 12*len(sequentialMapGroup)
        numGroups = len(sequentialMapGroup)

        beginning = struct.pack(">HHIII"
                                , self.format # UInt16
                                , 0 # Reserved, UInt16
                                , subtableLength # UInt32
                                , self.language # UInt32
                                , numGroups # UInt32
                                )

        smgBytes = b''

        for smg in sequentialMapGroup:
            smgBytes += smg.toBytes()

        return beginning + smgBytes



class cmapFormat14:
    """
    Class representing cmap subtable format 14.
    (Subtable indicating the usage of variation selectors.)

    This is only capable of implementing Variation Selector 16 (U+FE0F) right now.

    - https://docs.microsoft.com/en-us/typography/opentype/spec/cmap#format-14-unicode-variation-sequences
    """

    def __init__(self, glyphs, platformID, platEncID):
        self.glyphs = glyphs
        self.platformID = platformID
        self.platEncID = platEncID


    def toTTX(self):
        cmap14 = Element("cmap_format_14",    { "platformID": str(self.platformID)
                                                , "platEncID": str(self.platEncID)
                                                , "format": "14"
                                                , "length": "0"
                                                , "numVarSelectorRecords": "1"
                                                })

        for g in self.glyphs:
            if not g.alias:
                cmap14.append(Element("map", {"uvs": "0xfe0f", "uv": hex(g.codepoints.seq[0]), "name": g.name()}))
            else:
                cmap14.append(Element("map", {"uvs": "0xfe0f", "uv": hex(g.codepoints.seq[0]), "name": g.alias.name()}))

        return cmap14

    def toBytes(self):
        return b'' # placeholder

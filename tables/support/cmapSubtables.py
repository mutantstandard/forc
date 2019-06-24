import struct
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
        glyphIdArrayInt = [0x00] * 256 # MAYBE: I presume that no value is 0x00.

        for id, glyph in self.glyphs:
            glyphIdArray[id] = glyph.codepoints.sequence[0]


        # TODO: store ints in this bytearray properly.
        glyphIdArray = bytearray()

        for int in glyphID:
            glyphIdArray.append(int)

        return beginning + glyphIdArray




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
        for id, glyph in self.glyphs.items():
            thisGlyphCodepoint = glyph.codepoints.sequence[0]
            lastGlyphCodepoint = glyphs[id-1].codepoints.sequence[0]

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


        # Generate a bunch of metadata. these calculations are what they are.
        segCountX2 = segCount * 2
        searchRange = 2 * (2 ** floor(log2(39)))
        entrySelector = log2(searchRange / 2)
        rangeShift = 2 * segCount - searchRange

        beginning = struct.pack( ">HHHHHHHHHHhH"
                          , self.format # UInt16
                          # length # UInt16
                          , self.language # UInt16
                          , segCountX2 # UInt16
                          , searchRange # UInt16
                          , entrySelector # UInt16
                          , rangeShift # UInt16
                          )

        # TODO: create bytes representations of these and compile.

                          # endCode[segCount] # UInt16. End character code for each segment. Last possible one = 0xFFFF
                          # reservedPad = 0. UInt16
                          # startCode[segCount] # UInt16. Start character code for each segment.
                          # idDelta[segCount] # Int16. Delta for all character codes in the segment.
                          # idRangeOffset[segCount] # UInt16. Offsets into glyphIdArray or 0.
                          # glyphIdArray[] # Array of UInt16s.



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

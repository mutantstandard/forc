import struct
from lxml.etree import Element
from tables.support.os2Extra import panose





class os2:
    """
    Class representing an OS/2 table.
    """

    def __init__(self, m, glyphs):

        # PREPARE DATA
        # --------------------------

        metrics = m['metrics']

        singleCodepoints = []
        twoByte = []

        # the only bit in ulUnicodeRange that's *really* necessary to set.
        supplementaryPlane = False

        for g in glyphs['all']:
            if g.codepoints.seq[0] >= int('0x10000', 16) and g.codepoints.seq[0] <= int('0x10ffff', 16):
                supplementaryPlane = True

            if len(g.codepoints.seq) == 1:
                singleCodepoints.append(g.codepoints.seq[0])

                if g.codepoints.seq[0] < int('ffff', 16):
                    twoByte.append(g.codepoints.seq[0])

        usFirstCharIndex = hex(min(twoByte))
        usLastCharIndex = hex(max(twoByte))



        # STORE DATA
        # --------------------------

        self.version = 5 # hard-coded, the current (also the latest) version for this table generation is 5.

        self.xAvgCharWidth = metrics['xMax']
        self.usWeightClass = 500 # hard-coded for now. This is ideal for emoji.
        self.usWidthClass = 5 # hard-coded for now. This is ideal for emoji.

        self.fsType = '00000000 00000000'
        # self.fsType = int('00000000' '00000000', 2) # hard-coded. must agree with head.macStyle

        self.ySubscriptXSize = metrics['OS2ySubscriptXSize']
        self.ySubscriptYSize = metrics['OS2ySubscriptYSize']
        self.ySubscriptXOffset = metrics['OS2ySubscriptXOffset']
        self.ySubscriptYOffset = metrics['OS2ySubscriptYOffset']

        self.ySuperscriptXSize = metrics['OS2ySuperscriptXSize']
        self.ySuperscriptYSize = metrics['OS2ySuperscriptYSize']
        self.ySuperscriptXOffset = metrics['OS2ySuperscriptXOffset']
        self.ySuperscriptYOffset = metrics['OS2ySuperscriptYOffset']

        self.yStrikeoutSize = metrics['OS2yStrikeoutSize']
        self.yStrikeoutPosition = metrics['OS2yStrikeoutPosition']

        self.sFamilyClass = 5 # hard-coded for now. This is ideal for emoji.

        self.panose = panose(2, 0, 6, 9, 0, 0, 0, 0, 0, 0)

        self.ulUnicodeRange1 = '00000000 00000000 00000000 00000000'
        self.ulUnicodeRange2 = '000000'+ str(int(supplementaryPlane)) + '0 00000000 00000000 00000000'
        self.ulUnicodeRange3 = '00000000 00000000 00000000 00000000'
        self.ulUnicodeRange4 = '00000000 00000000 00000000 00000000'
        # self.ulUnicodeRange1 = int('00000000' '00000000' '00000000' '00000000', 2)
        # self.ulUnicodeRange2 = int('000000'+ str(int(supplementaryPlane)) + '0' '00000000' '00000000' '00000000', 2)
        # self.ulUnicodeRange3 = int('00000000' '00000000' '00000000' '00000000', 2)
        # self.ulUnicodeRange4 = int('00000000' '00000000' '00000000' '00000000', 2)

        # TODO: convert this into a real Tag data format at the very beginning.
        # probably make your own data type to cover for this.
        self.achVendID = m['metadata']['OS2VendorID']

        self.fsSelection = '00000000 00000000' # hard-coded
        # self.fsSelection = int('00000000' '00000000', 2)

        self.usFirstCharIndex = usFirstCharIndex
        self.usLastCharIndex = usLastCharIndex

        self.sTypoAscender = metrics['yMax']
        self.sTypoDescender = metrics['yMin'] # this should be this way based on validators and best practices.
        self.sTypoLineGap = 0 # hard-coded based on best practices.
        self.usWinAscent = metrics['yMax']
        self.usWinDescent = (- metrics['yMin']) # should be -yMin: https://docs.microsoft.com/en-us/typography/opentype/spec/os2#uswindescent

        self.ulCodePageRange1 = '00000000 00000000 00000000 00000000'
        self.ulCodePageRange2 = '00000000 00000000 00000000 00000000'
        # self.ulCodePageRange1 = int('00000000' '00000000' '00000000' '00000000', 2)
        # self.ulCodePageRange2 = int('00000000' '00000000' '00000000' '00000000', 2)

        self.sxHeight = 0 # leaving it hard-coded at 0 for now.
        self.sCapHeight = metrics['yMax']

        self.usDefaultChar = 0
        self.usBreakChar = 0x20
        self.usMaxContent = 1

        self.usLowerOpticalPointSize = 0
        self.usUpperOpticalPointSize = 0



    def toTTX(self):
        """
        Outputs table to TTX format.
        """

        os2 = Element("OS_2")

        os2.append(Element("version", {'value': '5'})) # hard-coded

        os2.append(Element("xAvgCharWidth", {'value': str(self.xAvgCharWidth) }))
        os2.append(Element("usWeightClass", {'value': str(self.usWeightClass) }))
        os2.append(Element("usWidthClass", {'value': str(self.usWidthClass) }))

        # TODO: This is unfinished, work on it more later.
        # os2.append(Element("fsType", {'value': str(struct.pack(">H", self.fsType)) })) # convert to binary string
        os2.append(Element("fsType", {'value': self.fsType })) # convert to binary string

        os2.append(Element("ySubscriptXSize", {'value': str(self.ySubscriptXSize) }))
        os2.append(Element("ySubscriptYSize", {'value': str(self.ySubscriptYSize) }))
        os2.append(Element("ySubscriptXOffset", {'value': str(self.ySubscriptXOffset) }))
        os2.append(Element("ySubscriptYOffset", {'value': str(self.ySubscriptYOffset) }))

        os2.append(Element("ySuperscriptXSize", {'value': str(self.ySuperscriptXSize) }))
        os2.append(Element("ySuperscriptYSize", {'value': str(self.ySuperscriptYSize) }))
        os2.append(Element("ySuperscriptXOffset", {'value': str(self.ySuperscriptXOffset) }))
        os2.append(Element("ySuperscriptYOffset", {'value': str(self.ySuperscriptYOffset) }))

        os2.append(Element("yStrikeoutSize", {'value': str(self.yStrikeoutSize) }))
        os2.append(Element("yStrikeoutPosition", {'value': str(self.yStrikeoutPosition) }))



        os2.append(Element("sFamilyClass", {'value': str(self.sFamilyClass) }))


        os2.append(self.panose.toTTX())


        # TODO: This is unfinished, work on it more later.
        # reminder: TTX takes in binary literals in Big-endian format.
        os2.append(Element("ulUnicodeRange1", {'value': self.ulUnicodeRange1 }))
        os2.append(Element("ulUnicodeRange2", {'value': self.ulUnicodeRange2 }))
        os2.append(Element("ulUnicodeRange3", {'value': self.ulUnicodeRange3 }))
        os2.append(Element("ulUnicodeRange4", {'value': self.ulUnicodeRange4 }))

        os2.append(Element("achVendID", {'value': str(self.achVendID) }))

        os2.append(Element("fsSelection", {'value': self.fsSelection }))

        # TTX actually cannibalises this input, but it's going to input them anyway.
        os2.append(Element("usFirstCharIndex", {'value': str(self.usFirstCharIndex) }))
        os2.append(Element("usLastCharIndex", {'value': str(self.usLastCharIndex) }))

        os2.append(Element("sTypoAscender", {'value': str(self.sTypoAscender) }))
        os2.append(Element("sTypoDescender", {'value': str(self.sTypoDescender) }))
        os2.append(Element("sTypoLineGap", {'value': str(self.sTypoLineGap) }))
        os2.append(Element("usWinAscent", {'value': str(self.usWinAscent) }))
        os2.append(Element("usWinDescent", {'value': str(self.usWinDescent) }))

        os2.append(Element("ulCodePageRange1", {'value': self.ulCodePageRange1 }))
        os2.append(Element("ulCodePageRange2", {'value': self.ulCodePageRange2 }))

        os2.append(Element("sxHeight", {'value': str(self.sxHeight) }))
        os2.append(Element("sCapHeight", {'value': str(self.sCapHeight) }))

        os2.append(Element("usDefaultChar", {'value': str(self.usDefaultChar) }))
        os2.append(Element("usBreakChar", {'value': str(hex(self.usBreakChar)) }))
        os2.append(Element("usMaxContext", {'value': str(self.usMaxContent) }))

        os2.append(Element("usLowerOpticalPointSize", {'value': str(self.usLowerOpticalPointSize) }))
        os2.append(Element("usUpperOpticalPointSize", {'value': str(self.usUpperOpticalPointSize) }))

        return os2




    def toBinary(self):
        """
        Outputs table to binary, formatted for sfnt.
        """

        return struct.pack( ">hhHHHhhhhhhhhhhhbIIIIIHHHhhhHHHHhhHHHHH"
                          , self.version # UInt16

                          , self.xAvgCharWidth # Int16
                          , self.usWeightClass # UInt16
                          , self.usWidthClass # UInt16

                          , self.fsType # UInt16

                          , self.ySubscriptXSize # Int16
                          , self.ySubscriptYSize # Int16
                          , self.ySubscriptXOffset # Int16
                          , self.ySubscriptYOffset # Int16

                          , self.ySuperscriptXSize # Int16
                          , self.ySuperscriptYSize # Int16
                          , self.ySuperscriptXOffset # Int16
                          , self.ySuperscriptYOffset # Int16

                          , self.yStrikeoutSize # Int16
                          , self.yStrikeoutPosition # Int16

                          , self.sFamilyClass # Int16

                          , self.panose.toBinary() # 10 UInt16s. TODO: Dunno how to do this.

                          , self.ulUnicodeRange1 # UInt32
                          , self.ulUnicodeRange2 # UInt32
                          , self.ulUnicodeRange3 # UInt32
                          , self.ulUnicodeRange4 # UInt32

                          , int(self.achVendID) # Tag (UInt32)

                          , self.fsSelection # UInt16

                          , self.usFirstCharIndex # UInt16
                          , self.usLastCharIndex # UInt16

                          , self.sTypoAscender # Int16
                          , self.sTypoDescender # Int16
                          , self.sTypoLineGap # Int16
                          , self.usWinAscent # UInt16
                          , self.usWinDescent # UInt16

                          , self.ulCodePageRange1 # UInt32
                          , self.ulCodePageRange2 # UInt32

                          , self.sxHeight # Int16
                          , self.sCapHeight # Int16

                          , self.usDefaultChar # UInt16
                          , self.usBreakChar # UInt16
                          , self.usMaxContent # UInt16

                          , self.usLowerOpticalPointSize # UInt16
                          , self.usUpperOpticalPointSize # UInt16
                          )

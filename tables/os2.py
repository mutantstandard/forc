import struct
from lxml.etree import Element

from data import BFlags
from tables.support.os2Extra import PANOSE





class OS2:
    """
    Class representing an OS/2 table.
    """

    def __init__(self, m, glyphs):

        # PREPARE SOME OF THE DATA
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

        self.fsType = BFlags('00000000 00000000') # hard-coded. must agree with head.macStyle

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

        self.panose = PANOSE(2, 0, 6, 9, 0, 0, 0, 0, 0, 0)

        self.ulUnicodeRange1 = BFlags('00000000 00000000 00000000 00000000')
        self.ulUnicodeRange2 = BFlags('00000000 00000000 00000000 00000000')
        self.ulUnicodeRange2.set(57-32, int(supplementaryPlane))

        self.ulUnicodeRange3 = BFlags('00000000 00000000 00000000 00000000')
        self.ulUnicodeRange4 = BFlags('00000000 00000000 00000000 00000000')

        self.achVendID = m['metadata']['OS2VendorID']

        self.fsSelection = BFlags('00000000 00000000') # hard-coded

        self.usFirstCharIndex = usFirstCharIndex
        self.usLastCharIndex = usLastCharIndex

        self.sTypoAscender = metrics['yMax']
        self.sTypoDescender = metrics['yMin'] # this should be this way based on validators and best practices.
        self.sTypoLineGap = 0 # hard-coded based on best practices.
        self.usWinAscent = metrics['yMax']
        self.usWinDescent = (- metrics['yMin']) # this should be the way it is (-yMin): https://docs.microsoft.com/en-us/typography/opentype/spec/os2#uswindescent

        self.ulCodePageRange1 = BFlags('00000000 00000000 00000000 00000000')
        self.ulCodePageRange2 = BFlags('00000000 00000000 00000000 00000000')

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

        os2.append(Element("version", {'value': str(self.version) }))

        os2.append(Element("xAvgCharWidth", {'value': str(self.xAvgCharWidth) }))
        os2.append(Element("usWeightClass", {'value': str(self.usWeightClass) }))
        os2.append(Element("usWidthClass", {'value': str(self.usWidthClass) }))

        os2.append(Element("fsType", {'value': self.fsType.toTTXStr() }))

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


        os2.append(Element("ulUnicodeRange1", {'value': self.ulUnicodeRange1.toTTXStr() }))
        os2.append(Element("ulUnicodeRange2", {'value': self.ulUnicodeRange2.toTTXStr() }))
        os2.append(Element("ulUnicodeRange3", {'value': self.ulUnicodeRange3.toTTXStr() }))
        os2.append(Element("ulUnicodeRange4", {'value': self.ulUnicodeRange4.toTTXStr() }))

        os2.append(Element("achVendID", {'value': str(self.achVendID) }))

        os2.append(Element("fsSelection", {'value': self.fsSelection.toTTXStr() }))

        # TTX actually cannibalises these two, but forc is going to input them anyway.
        os2.append(Element("usFirstCharIndex", {'value': str(self.usFirstCharIndex) }))
        os2.append(Element("usLastCharIndex", {'value': str(self.usLastCharIndex) }))

        os2.append(Element("sTypoAscender", {'value': str(self.sTypoAscender) }))
        os2.append(Element("sTypoDescender", {'value': str(self.sTypoDescender) }))
        os2.append(Element("sTypoLineGap", {'value': str(self.sTypoLineGap) }))
        os2.append(Element("usWinAscent", {'value': str(self.usWinAscent) }))
        os2.append(Element("usWinDescent", {'value': str(self.usWinDescent) }))

        os2.append(Element("ulCodePageRange1", {'value': self.ulCodePageRange1.toTTXStr() }))
        os2.append(Element("ulCodePageRange2", {'value': self.ulCodePageRange2.toTTXStr() }))

        os2.append(Element("sxHeight", {'value': str(self.sxHeight) }))
        os2.append(Element("sCapHeight", {'value': str(self.sCapHeight) }))

        os2.append(Element("usDefaultChar", {'value': str(self.usDefaultChar) }))
        os2.append(Element("usBreakChar", {'value': str(hex(self.usBreakChar)) }))
        os2.append(Element("usMaxContext", {'value': str(self.usMaxContent) }))

        os2.append(Element("usLowerOpticalPointSize", {'value': str(self.usLowerOpticalPointSize) }))
        os2.append(Element("usUpperOpticalPointSize", {'value': str(self.usUpperOpticalPointSize) }))

        return os2




    def toBytes(self):
        """
        Outputs table to bytes, formatted for sfnt.
        """

        return struct.pack( ">hhHH2bhhhhhhhhhhh10b4b4b4b4b4b2bHHhhhHH4b4bhhHHHHH"
                          , self.version # UInt16

                          , self.xAvgCharWidth # Int16
                          , self.usWeightClass # UInt16
                          , self.usWidthClass # UInt16

                          , self.fsType.toBytes() # 2 bytes/UInt16

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

                          , self.panose.toBytes() # 10 byte/10 UInt16s.

                          , self.ulUnicodeRange1.toBytes() # 4 bytes/UInt32
                          , self.ulUnicodeRange2.toBytes() # 4 bytes/UInt32
                          , self.ulUnicodeRange3.toBytes() # 4 bytes/UInt32
                          , self.ulUnicodeRange4.toBytes() # 4 bytes/UInt32

                          , self.achVendID.toBytes() # Tag (4 bytes/UInt32)

                          , self.fsSelection.toBytes() # 2 bytes/UInt16

                          , self.usFirstCharIndex # UInt16
                          , self.usLastCharIndex # UInt16

                          , self.sTypoAscender # Int16
                          , self.sTypoDescender # Int16
                          , self.sTypoLineGap # Int16
                          , self.usWinAscent # UInt16
                          , self.usWinDescent # UInt16

                          , self.ulCodePageRange1.toBytes() # 4 bytes/UInt32
                          , self.ulCodePageRange2.toBytes() # 4 bytes/UInt32

                          , self.sxHeight # Int16
                          , self.sCapHeight # Int16

                          , self.usDefaultChar # UInt16
                          , self.usBreakChar # UInt16
                          , self.usMaxContent # UInt16

                          , self.usLowerOpticalPointSize # UInt16
                          , self.usUpperOpticalPointSize # UInt16
                          )

import struct
from lxml.etree import Element

from data import vFixed

class hhea:
    """
    Class representing an hhea table.
    """

    def __init__(self, m):

        metrics = m['metrics']

        self.majorVersion = 1
        self.minorVersion = 0

        self.ascent = metrics['horiAscent']
        self.descent = metrics['horiDescent']
        self.lineGap = 0 # hard-coded based on best practices

        self.advanceWidthMax = metrics['xMax']
        self.minLeftSideBearing = 0
        self.minRightSideBearing = metrics['xMax']
        self.xMaxExtent = 0

        # carets should be this ratio for emoji fonts.
        self.caretSlopeRise = 1
        self.caretSlopeRun = 0
        self.caretOffset = 0

        # reserved, hardcoded; meant to be 0.
        self.reserved0 = 0
        self.reserved1 = 0
        self.reserved2 = 0
        self.reserved3 = 0

        self.metricDataFormat = 0 # hardcoded, meant to be 0.
        self.numberofHMetrics = 0 # TODO: try to actually generate this based on the actual number of hmetrics that exist.



    def toTTX(self):
        """
        Compiles table to TTX.
        """

        hhea = Element("hhea")

        hhea.append(Element("tableVersion", {'value': vFixed(f"{self.majorVersion}.{self.minorVersion}").toHexStr() })) # TTX wants the version in this format.

        hhea.append(Element("ascent", {'value': str(self.ascent) }))
        hhea.append(Element("descent", {'value': str(self.descent) }))
        hhea.append(Element("lineGap", {'value': str(self.lineGap) }))

        hhea.append(Element("advanceWidthMax", {'value': str(self.advanceWidthMax) }))
        hhea.append(Element("minLeftSideBearing", {'value': str(self.minLeftSideBearing) }))
        hhea.append(Element("minRightSideBearing", {'value': str(self.minRightSideBearing) }))
        hhea.append(Element("xMaxExtent", {'value': str(self.xMaxExtent) }))

        hhea.append(Element("caretSlopeRise", {'value': str(self.caretSlopeRise) }))
        hhea.append(Element("caretSlopeRun", {'value': str(self.caretSlopeRun) }))
        hhea.append(Element("caretOffset", {'value': str(self.caretOffset) }))


        hhea.append(Element("reserved0", {'value': str(self.reserved0) }))
        hhea.append(Element("reserved1", {'value': str(self.reserved1) }))
        hhea.append(Element("reserved2", {'value': str(self.reserved2) }))
        hhea.append(Element("reserved3", {'value': str(self.reserved3) }))

        hhea.append(Element("metricDataFormat", {'value': str(self.metricDataFormat) }))
        hhea.append(Element("numberOfHMetrics", {'value': str(self.numberofHMetrics) }))

        return hhea


    def toBinary(self):
        return struct.pack('>HHhhhHhhhhhhhhhhhH'
                          , self.majorVersion # UInt16
                          , self.minorVersion # UInt16

                          , self.ascent # Int16
                          , self.descent # Int16
                          , self.lineGap # Int16

                          , self.advanceWidthMax # UInt16 (yep, definitely unsigned)
                          , self.minLeftSideBearing # Int16
                          , self.minRightSideBearing # Int16
                          , self.xMaxExtent # Int16

                          , self.caretSlopeRise # Int16
                          , self.caretSlopeRun # Int16
                          , self.caretOffset # Int16

                          , self.reserved0 # Int16
                          , self.reserved1 # Int16
                          , self.reserved2 # Int16
                          , self.reserved3 # Int16

                          , self.metricDataFormat # Int16
                          , self.numberofHMetrics # UInt16
                          )

import struct
from lxml.etree import Element


class vhea:
    """
    Class representing a vhea table.
    """

    def __init__(self, m):

        metrics = m['metrics']

        self.version = '0x00010000' # hard-coded    TODO: put it in a more accurate data format.

        self.ascent = metrics['vertAscent']
        self.descent = metrics['vertDescent']
        self.lineGap = 0 # hard-coded based on best practices

        self.advanceHeightMax = metrics['height']
        self.minTopSideBearing = 0
        self.minBottomSideBearing = 0
        self.yMaxExtent = metrics['height']

        # carets should be this ratio for emoji fonts.
        self.caretSlopeRise = 1
        self.caretSlopeRun = 0
        self.caretOffset = 0

        # reserved, hardcoded; meant to be 0.
        # yes, the numbers are different from hhea. That's meant to be the case.
        self.reserved1 = 0
        self.reserved2 = 0
        self.reserved3 = 0
        self.reserved4 = 0

        self.metricDataFormat = 0 # hardcoded, meant to be 0.
        self.numOfLongVerMetrics = 0 # TODO: try to actually generate this based on the actual number of vmetrics that exist.



    def toTTX(self):
        """
        Compiles table to TTX.
        """

        vhea = Element("vhea")

        vhea.append(Element("tableVersion", {'value': self.version }))

        vhea.append(Element("ascent", {'value': str(self.ascent) }))
        vhea.append(Element("descent", {'value': str(self.descent) }))
        vhea.append(Element("lineGap", {'value': str(self.lineGap) }))

        vhea.append(Element("advanceHeightMax", {'value': str(self.advanceHeightMax) }))
        vhea.append(Element("minTopSideBearing", {'value': str(self.minTopSideBearing) }))
        vhea.append(Element("minBottomSideBearing", {'value': str(self.minBottomSideBearing) }))
        vhea.append(Element("yMaxExtent", {'value': str(self.yMaxExtent) }))

        vhea.append(Element("caretSlopeRise", {'value': str(self.caretSlopeRise) }))
        vhea.append(Element("caretSlopeRun", {'value': str(self.caretSlopeRun) }))
        vhea.append(Element("caretOffset", {'value': str(self.caretOffset) }))

        vhea.append(Element("reserved1", {'value': str(self.reserved1) }))
        vhea.append(Element("reserved2", {'value': str(self.reserved2) }))
        vhea.append(Element("reserved3", {'value': str(self.reserved3) }))
        vhea.append(Element("reserved4", {'value': str(self.reserved4) }))

        vhea.append(Element("metricDataFormat", {'value': str(self.metricDataFormat) }))
        # I think it's supposed to be called this way. *shrugs*
        vhea.append(Element("numberOfHMetrics", {'value': str(self.numOfLongVerMetrics) }))

        return vhea



    def toBinary(self):
        return struct.pack(">ihhhhhhhhhhhhhhhH"
                          , self.version # Fixed (Int32, fixed-point)

                          , self.ascent # Int16
                          , self.descent # Int16
                          , self.lineGap # Int16

                          , self.advanceHeightMax # Int16
                          , self.minTopSideBearing # Int16
                          , self.minBottomSideBearing # Int16
                          , self.yMaxExtent # Int16

                          , self.caretSlopeRise # Int16
                          , self.caretSlopeRun # Int16
                          , self.caretOffset # Int16

                          , self.reserved1 # Int16
                          , self.reserved2 # Int16
                          , self.reserved3 # Int16
                          , self.reserved4 # Int16

                          , self.metricDataFormat # Int16
                          , self.numOfLongVerMetrics # UInt16
                          )

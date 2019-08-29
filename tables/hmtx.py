import struct
from lxml.etree import Element

from transform.bytes import padTableBytes



class hmtxMetric:
    """
    Class representing a single metric in an hmtx table.
    """

    def __init__(self, name, advanceWidth, lsb):
        self.name = name
        self.advanceWidth = advanceWidth
        self.lsb = lsb

    def toTTX(self):
        return Element("mtx", {"name": self.name
                                ,"width": str(self.advanceWidth)
                                ,"lsb": str(self.lsb)
                                })

    def toBytes(self):
        return struct.pack(">Hh"
                          , self.advanceWidth
                          , self.lsb
                          )



class hmtx:
    """
    Class representing an hmtx table.
    """
    def __init__(self, m, glyphs):

        self.metrics = []

        for g in glyphs["img_empty"]:
            self.metrics.append(hmtxMetric(g.name(), m['metrics']['normalWidth'], m['metrics']['normalLSB']))

    def toTTX(self):
        hmtx = Element("hmtx")

        for m in self.metrics:
            hmtx.append(m.toTTX())

        return hmtx

    def toBytes(self):
        longHorMetric = b''
        for m in self.metrics:
            longHorMetric += m.toBytes()

        return padTableBytes(longHorMetric)

        # TODO: work out how to calcuilate leftSideBearings[numGlyphs - numberOfHMetrics]
        # https://docs.microsoft.com/en-us/typography/opentype/spec/hmtx

from lxml.etree import Element


class hmtxMetric:
    """
    Class representing a single metric in an hmtx table.
    """

    def __init__(self, name, width, lsb):
        self.name = name
        self.width = width
        self.LSB = lsb

    def toTTX(self):
        return Element("mtx", {"name": self.name
                                ,"width": str(self.width)
                                ,"lsb": str(self.LSB)
                                })



class hmtx:
    """
    Class representing an hmtx table.
    """
    def __init__(self, m, glyphs):

        self.tableName = "hmtx" # hard-coded. For font generation only.
        self.metrics = []

        for g in glyphs["img_empty"]:
            self.metrics.append(hmtxMetric(g.name(), m['metrics']['normalWidth'], m['metrics']['normalLSB']))

    def toTTX(self):
        hmtx = Element("hmtx")

        for m in self.metrics:
            hmtx.append(m.toTTX())

        return hmtx

    def toBytes(self):
        return bytes()#temp

    # TODO: figure out how to convert hmtx to bytes.

from lxml.etree import Element


class vmtxMetric:
    """
    Class representing a single metric in a vmtx table.
    """

    def __init__(self, name, height, tsb):
        self.name = name
        self.height = height
        self.TSB = tsb

    def toTTX(self):
        return Element("mtx", {"name": self.name
                                ,"height": str(self.height)
                                ,"tsb": str(self.TSB)
                                })



class vmtx:
    """
    Class representing a vmtx table.
    """
    def __init__(self, m, glyphs):
        self.metrics = []

        for g in glyphs["img_empty"]:
            self.metrics.append(vmtxMetric(g.codepoints.name(), m['metrics']['normalHeight'], m['metrics']['normalTSB']))

    def toTTX(self):
        vmtx = Element("vmtx")

        for m in self.metrics:
            vmtx.append(m.toTTX())

        return vmtx

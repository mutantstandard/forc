from lxml.etree import Element


class gasp:
    """
    Class representing a placeholder gasp table.
    """

    def __init__(self):

        self.rangeMaxPPEM = 65535
        self.rangeGaspBehavior = 0x0f

    def toTTX(self):
        """
        Create a really basic gasp table.
        """

        gasp = Element("gasp")

        gasp.append(Element("gaspRange", {'rangeMaxPPEM': str(self.rangeMaxPPEM)
                                         ,'rangeGaspBehavior': hex(self.rangeGaspBehavior)
                                         }))

        return gasp

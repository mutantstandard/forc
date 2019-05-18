from lxml.etree import Element



class dsig:
    """
    Class representing a placeholder DSIG table.
    """

    def __init__(self):

        # all the data here is just formatted for TTX output atm.
        self.version = '0x00000001'
        self.flag = '00000000'
        self.numSigs = 0


    def toTTX(self):
        """
        Create a dummy DSIG table.
        """

        dsig = Element("DSIG")

        dsig.append(Element("tableHeader", {'version': self.version
                                           ,'flag': self.flag
                                           ,'numSigs': str(self.numSigs)
                                           }))

        return dsig

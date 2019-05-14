from lxml.etree import Element

class head:
    """
    Class representing a 'head' table.
    """

    def __init__(self, m):


        # creating an OpenType-compliant fontRevision number based on best practices.
        # https://silnrsi.github.io/FDBP/en-US/Versioning.html
        versionComponents = m['metadata']['version'].split('.')

        try:
            majorVersion = int(versionComponents[0])
            minorVersion = int(( int(versionComponents[1]) / 1000 ) * 65536)
        except:
            raise Exception("Converting headVersion to it's proper data structure failed for some reason!" + str(e))

        headVersionHex = '0x{0:0{1}X}'.format(majorVersion, 4) + '{0:0{1}X}'.format(minorVersion, 4)




        self.tableVersion = 1.0 # hard-coded
        self.fontRevision = headVersionHex
        self.fontRevisionTTXfriendly = m['metadata']['version'] # TTX is weird about font versioning, only accepts a basic string.

        self.checkSumAdjustment = 0 # this is only set at compilation.
        self.magicNumber = "0x5f0f3cf5" # hard-coded

        self.flags = '00000000 00001011' # hard-coded    TODO: Work on a more accurate format for internal use.

        self.unitsPerEm = m['metrics']['unitsPerEm']
        self.created = m['metadata']['created'] #TODO: Work on a more accurate format for internal use.
        self.modified = 'Mon Dec 11 13:45:00 2018' #TODO: Work on a more accurate format for internal use.

        self.xMin = m['metrics']['xMin']
        self.yMin = m['metrics']['yMin']
        self.xMax = m['metrics']['xMax']
        self.yMax = m['metrics']['yMax']

        self.macStyle = '00000000 00000000' # hard-coded. Must agree with OS/2's fsType. TODO: Work on a more accurate format for internal use.
        self.lowestRecPPEM = m['metrics']['lowestRecPPEM']

        self.fontDirectionHint = 2 # depreciated, hard-coded
        self.indexToLocFormat = 0 # not important, hard-coded
        self.glyphDataFormat = 0 # not important, hard-coded





    def toTTX(self):
        """
        Compiles table to TTX.
        """

        head = Element("head")

        head.append(Element("tableVersion", {'value': str(self.tableVersion) }))
        head.append(Element("fontRevision", {'value': str(self.fontRevisionTTXfriendly)  })) # have to use the TTX-friendly version

        head.append(Element("checkSumAdjustment", {'value': str(self.checkSumAdjustment) })) # TTX changes this at compilation
        head.append(Element("magicNumber", {'value': str(self.magicNumber) }))

        head.append(Element("flags", {'value': self.flags }))

        head.append(Element("unitsPerEm", {'value': str( self.unitsPerEm )}))
        head.append(Element("created", {'value':  self.created }))
        head.append(Element("modified", {'value': self.modified })) # TTX changes this at compilation *shrugs*

        head.append(Element("xMin", {'value': str(self.xMin) }))
        head.append(Element("yMin", {'value': str(self.yMin) }))
        head.append(Element("xMax", {'value': str(self.xMax) }))
        head.append(Element("yMax", {'value': str(self.yMax) }))

        head.append(Element("macStyle", {'value': self.macStyle }))
        head.append(Element("lowestRecPPEM", {'value': str(self.lowestRecPPEM) }))

        head.append(Element("fontDirectionHint", {'value': str(self.fontDirectionHint) }))
        head.append(Element("indexToLocFormat", {'value': str(self.indexToLocFormat) }))
        head.append(Element("glyphDataFormat", {'value': str(self.glyphDataFormat) }))

        return head

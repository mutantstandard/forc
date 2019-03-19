from lxml.etree import Element

def create():
    """
    Create a dummy DSIG table.
    """

    dsig = Element("DSIG")

    dsig.append(Element("tableHeader", {'version': '0x00000001'
                                       ,'flag': '00000000'
                                       ,'numSigs': '0'
                                       }))

    return dsig

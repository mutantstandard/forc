from xml.etree.ElementTree import Element, tostring

from tables.glyphOrder import glyphOrder
from tables.head import head
from tables.os2 import os2
from tables.post import post
from tables.name import name
from tables.maxp import maxp
from tables.horizontalMetrics import hhea, hmtx
from tables.verticalMetrics import vhea, vmtx
from tables.cmap import cmap



def assembler(m):
    """
    Assembles the TTX file using the manifest file and input data.
    """
    # defining various variables that will get used in each table.

    metrics = m['metrics']

    created = m['metadata']['created']
    OS2VendorID = m['metadata']['OS2VendorID']
    nameRecords = m['metadata']['nameRecords']


    macLangID = m['encoding']['macLangID']
    msftLangID = m['encoding']['msftLangID']



    # start the TTX file
    root = Element('ttFont')
    root.attrib = {'sfntVersion': '\\x00\\x01\\x00\\x00', 'ttLibVersion': '3.28'} # hard-coded attrs.

    # headers and other weird crap
    root.append(glyphOrder())
    root.append(head(metrics, created))
    root.append(os2(metrics, OS2VendorID))
    root.append(post())
    root.append(maxp())
    root.append(Element("loca")) # just to please macOS, it's supposed to be empty.

    # horizontal and vertical metrics tables
    root.append(hhea())
    root.append(hmtx())
    root.append(vhea())
    root.append(vmtx())

    # glyph-code mappings
    root.append(cmap(macLangID, msftLangID))
    # if ligatures
    # gdef()
    # gsub()
    # etc.


    # glyph picture data

    # glyf()

    # if svginot
    #   svg()
    # if sbix
    #   sbix()
    # if CBDT/CBLC
    #   cblc()
    #   cbdt()


    # human-readable metadata
    root.append(name(nameRecords, macLangID, msftLangID))



    return tostring(root, encoding="unicode", method="xml")

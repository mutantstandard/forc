from lxml.etree import Element, tostring

import log

from tables.glyphOrder import glyphOrder
from tables.head import head
from tables.os2 import os2
from tables.post import post
from tables.name import name
from tables.maxp import maxp

from tables.horizontalMetrics import hhea, hmtx
from tables.verticalMetrics import vhea, vmtx

from tables.cmap import cmap
from tables.glyf import glyf

from tables.svg import svg
from tables.sbix import sbix
from tables.cbdt import cbdt
from tables.cblc import cblc






def assembler(format, m, glyphs):
    """
    Assembles a TTX file using the manifest file and input data.
    """


    # defining various variables that will get used in each table.
    # just making this a bit more readable, basically.

    metrics = m['metrics']

    created = m['metadata']['created']
    OS2VendorID = m['metadata']['OS2VendorID']
    nameRecords = m['metadata']['nameRecords']

    macLangID = m['encoding']['macLangID']
    msftLangID = m['encoding']['msftLangID']



    # start the TTX file
    # ---------------------------------------------
    log.out(f'Assembling TTX file...')
    root = Element('ttFont', {'sfntVersion': '\\x00\\x01\\x00\\x00', 'ttLibVersion': '3.28'}) # hard-coded attrs.





    # headers and other weird crap
    # ---------------------------------------------
    log.out('Assembling glyphOrder list...', 36)
    root.append(glyphOrder(glyphs))

    log.out('Assembling head table...', 36)
    root.append(head(metrics, created))

    log.out('Assembling OS/2 table...', 36)
    root.append(os2(metrics, OS2VendorID))

    log.out('Assembling post table...', 36)
    root.append(post(glyphs))

    log.out('Making placeholder maxp table...', 36)
    root.append(maxp())

    log.out('Making placeholder loca table...', 36)
    root.append(Element("loca")) # just to please macOS, it's supposed to be empty.






    # horizontal and vertical metrics tables
    # ---------------------------------------------
    log.out('Assembling hhea table...', 36)
    root.append(hhea(metrics))

    log.out('Assembling hmtx table...', 36)
    root.append(hmtx(metrics, glyphs))

    log.out('Assembling vhea table...', 36)
    root.append(vhea(metrics))

    log.out('Assembling vmtx table...', 36)
    root.append(vmtx(metrics, glyphs))




    # glyph-code mappings
    # ---------------------------------------------
    log.out('Assembling cmap table...', 36)
    root.append(cmap(macLangID, msftLangID, glyphs))
    # if ligatures
    # gdef()
    # gsub()
    # etc.


    # glyph picture data
    # ---------------------------------------------

    root.append(glyf(glyphs))

    if format == "svginot":
        log.out('Assembling SVG table...', 36)
        root.append(svg(metrics, glyphs))

    elif format == "sbix":
        log.out('Assembling sbix table...', 36)
        root.append(sbix(glyphs))

    elif format == "cbx":
        log.out('Assembling CBLC table...', 36)
        root.append(cblc(metrics, glyphs))

        log.out('Assembling CBDT table...', 36)
        root.append(cbdt(metrics, glyphs))




    # human-readable metadata
    # ---------------------------------------------
    log.out('Assembling name table...', 36)
    root.append(name(format, macLangID, msftLangID, nameRecords))



    # the TTX is now done! (as long as something didn't go wrong)
    # return an XML string
    return tostring(root, pretty_print=True, method="xml", xml_declaration=True, encoding="UTF-8")

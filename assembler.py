from lxml.etree import Element, tostring

import log
from format import formats

from tables.glyphOrder import glyphOrder
from tables.head import head
from tables.os2  import os2
from tables.post import post
from tables.name import name
from tables.maxp import maxp

from tables.horizontalMetrics import hhea, hmtx
from tables.verticalMetrics import vhea, vmtx

from tables.cmap import cmap
from tables.gdef import gdef
from tables.gpos import gpos
from tables.gsub import gsub
from tables.morx import morx

from tables.glyf import glyf
from tables.svg  import svg
from tables.sbix import sbix
from tables.cbdt import cbdt
from tables.cblc import cblc






def assembler(chosenFormat, m, glyphs):
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
    log.out(f'Assembling root XML...', 90)
    root = Element('ttFont', {'sfntVersion': '\\x00\\x01\\x00\\x00', 'ttLibVersion': '3.28'}) # hard-coded attrs.





    # headers and other weird crap
    # ---------------------------------------------
    log.out('Assembling glyphOrder list...', 90)
    root.append(glyphOrder(glyphs))

    log.out('Assembling head table...', 90)
    root.append(head(m, created))

    log.out('Assembling OS/2 table...', 90)
    root.append(os2(OS2VendorID, metrics, glyphs))

    log.out('Assembling post table...', 90)
    root.append(post(glyphs))

    log.out('Making placeholder maxp table...', 90)
    root.append(maxp())

    log.out('Making placeholder loca table...', 90)
    root.append(Element("loca")) # just to please macOS, it's supposed to be empty.






    # horizontal and vertical metrics tables
    # ---------------------------------------------
    log.out('Assembling hhea table...', 90)
    root.append(hhea(metrics))

    log.out('Assembling hmtx table...', 90)
    root.append(hmtx(metrics, glyphs))

    log.out('Assembling vhea table...', 90)
    root.append(vhea(metrics))

    log.out('Assembling vmtx table...', 90)
    root.append(vmtx(metrics, glyphs))




    # glyph-code mappings
    # ---------------------------------------------

    # single glyphs
    log.out('Assembling cmap table...', 90)
    root.append(cmap(glyphs))



    # ligatures
    ligatures = False

    # check for presence of ligatures
    for g in glyphs:
        if len(g.codepoints) > 1:
            ligatures = True

    if ligatures:

        if formats[chosenFormat]["ligatureFormat"] == "OpenType":
            log.out ('Assembling GDEF table...', 90)
            root.append(gdef(glyphs))

            log.out ('Assembling GPOS table...', 90)
            root.append(gpos())

            log.out('Assembling GSUB table...', 90)
            root.append(gsub(glyphs))


        elif formats[chosenFormat]["ligatureFormat"] == "TrueType":
            log.out('Assembling morx table...', 90)
            root.append(morx(glyphs))




    # glyph picture data
    # ---------------------------------------------
    log.out('Assembling passable glyf table...', 90)
    root.append(glyf(glyphs))


    if formats[chosenFormat]["imageTables"] == "SVG":
        log.out('Assembling SVG table...', 90)
        root.append(svg(metrics, glyphs))

    elif formats[chosenFormat]["imageTables"] == "sbix":
        log.out('Assembling sbix table...', 90)
        root.append(sbix(glyphs))

    elif formats[chosenFormat]["imageTables"] == "CBx":
        log.out('Assembling CBLC table...', 90)
        root.append(cblc(metrics, glyphs))

        log.out('Assembling CBDT table...', 90)
        root.append(cbdt(metrics, glyphs))




    # human-readable metadata
    # ---------------------------------------------
    log.out('Assembling name table...', 90)
    root.append(name(chosenFormat, macLangID, msftLangID, nameRecords))



    # the TTX is now done! (as long as something didn't go wrong)
    # return an XML string
    return tostring(root, pretty_print=True, method="xml", xml_declaration=True, encoding="UTF-8")

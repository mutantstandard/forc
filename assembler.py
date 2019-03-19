from lxml.etree import Element, tostring

import log
from format import formats

import tables.glyphOrder
import tables.head
import tables.os2
import tables.post
import tables.name
import tables.maxp
import tables.gasp
import tables.dsig

import tables.mtx_h
import tables.mtx_v

import tables.cmap
import tables.gdef
import tables.gpos
import tables.gsub
import tables.morx

import tables.glyf
import tables.svg
import tables.sbix
import tables.cbdt
import tables.cblc






def assembler(chosenFormat, m, glyphs):
    """
    Assembles a TTX file using the manifest file and input data.
    """


    # start the TTX file
    # ---------------------------------------------
    log.out(f'Assembling root XML...', 90)
    root = Element('ttFont', {'sfntVersion': '\\x00\\x01\\x00\\x00', 'ttLibVersion': '3.28'}) # hard-coded attrs.




    # headers and other weird crap
    # ---------------------------------------------
    log.out('Assembling glyphOrder list...', 90)
    root.append(tables.glyphOrder.create(glyphs))

    log.out('Assembling head table...', 90)
    root.append(tables.head.create(m))

    log.out('Assembling OS/2 table...', 90)
    root.append(tables.os2.create(m, glyphs))

    log.out('Assembling post table...', 90)
    root.append(tables.post.create(glyphs))

    log.out('Making placeholder maxp table...', 90)
    root.append(tables.maxp.create())

    log.out('Making placeholder loca table...', 90)
    root.append(Element("loca")) # just to please macOS, it's supposed to be empty.

    log.out('Making gasp table...', 90)
    root.append(tables.gasp.create())

    log.out('Making placeholder DSIG table...', 90)
    root.append(tables.dsig.create())






    # horizontal and vertical metrics tables
    # ---------------------------------------------
    log.out('Assembling hhea table...', 90)
    root.append(tables.mtx_h.create_hhea(m))

    log.out('Assembling hmtx table...', 90)
    root.append(tables.mtx_h.create_hmtx(m, glyphs))

    log.out('Assembling vhea table...', 90)
    root.append(tables.mtx_v.create_vhea(m))

    log.out('Assembling vmtx table...', 90)
    root.append(tables.mtx_v.create_vmtx(m, glyphs))




    # glyph-code mappings
    # ---------------------------------------------

    # single glyphs
    log.out('Assembling cmap table...', 90)
    root.append(tables.cmap.create(glyphs))



    # ligatures
    ligatures = False

    # check for presence of ligatures
    for g in glyphs:
        if len(g) > 1:
            ligatures = True

    if ligatures:

        if formats[chosenFormat]["ligatureFormat"] == "OpenType":
            #log.out ('Assembling GDEF table...', 90)
            #root.append(tables.gdef.create(glyphs))

            #log.out ('Assembling GPOS table...', 90)
            #root.append(tables.gpos.create())

            log.out('Assembling GSUB table...', 90)
            root.append(tables.gsub.create(glyphs))


        elif formats[chosenFormat]["ligatureFormat"] == "TrueType":
            log.out('Assembling morx table...', 90)
            root.append(tables.morx.create(glyphs))




    # glyph picture data
    # ---------------------------------------------
    log.out('Assembling passable glyf table...', 90)
    root.append(tables.glyf.create(m, glyphs))


    if formats[chosenFormat]["imageTables"] == "SVG":
        log.out('Assembling SVG table...', 90)
        root.append(tables.svg.create(m, glyphs))

    elif formats[chosenFormat]["imageTables"] == "sbix":
        log.out('Assembling sbix table...', 90)
        root.append(tables.sbix.create(glyphs))

    elif formats[chosenFormat]["imageTables"] == "CBx":
        log.out('Assembling CBLC table...', 90)
        root.append(tables.cblc.create(m, glyphs))

        log.out('Assembling CBDT table...', 90)
        root.append(tables.cbdt.create(m, glyphs))




    # human-readable metadata
    # ---------------------------------------------
    log.out('Assembling name table...', 90)
    root.append(tables.name.create(chosenFormat, m))



    # the TTX is now done! (as long as something didn't go wrong)
    # return an XML string
    return tostring(root, pretty_print=True, method="xml", xml_declaration=True, encoding="UTF-8")

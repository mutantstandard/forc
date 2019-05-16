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

import tables.hhea
import tables.hmtx
import tables.vhea
import tables.vmtx

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






def assembler(chosenFormat, m, glyphs, flags):
    """
    Covers the entire routine for assembling a TTX file.
    """

    glyphFormat = formats[chosenFormat]["imageTables"]


    # start the TTX file
    # ---------------------------------------------
    root = Element('ttFont', {'sfntVersion': '\\x00\\x01\\x00\\x00', 'ttLibVersion': '3.28'}) # hard-coded attrs.



    # COLOR CODES:
    # 90 (gray):        a standard table that gets compiled no matter what.
    # 36 (dark cyan):   a table that is only compiled based on the font format.


    # headers and other weird crap
    # ---------------------------------------------
    log.out('[glyphOrder] ', 90, newline=False)
    root.append(tables.glyphOrder.toTTX(glyphs))

    log.out('[head] ', 90, newline=False)
    root.append(tables.head.head(m).toTTX())

    log.out('[OS/2] ', 90, newline=False)
    root.append(tables.os2.os2(m, glyphs).toTTX())

    log.out('[post] ', 90, newline=False)
    root.append(tables.post.toTTX(glyphs))

    # maxp is a semi-placeholder table.
    log.out('[maxp] ', 90, newline=False)
    root.append(tables.maxp.toTTX(glyphs))

    log.out('[gasp] ', 90, newline=False)
    root.append(tables.gasp.toTTX())




    # loca is a placeholder to make macOS happy.
    #
    # CBDT/CBLC either doesn't use loca or TTX doesn't want
    # an empty loca table if there's no gly table (CBDT/CBLC
    # fonts shouldnt have glyf tables.)

    if glyphFormat is not "CBx":
        log.out('[loca] ', 36, newline=False)
        root.append(Element("loca")) # just to please macOS, it's supposed to be empty.

    # placeholder table that makes Google's font validation happy.
    log.out('[DSIG]', 90)
    root.append(tables.dsig.toTTX())






    # horizontal and vertical metrics tables
    # ---------------------------------------------
    log.out('[hhea] ', 90, newline=False)
    root.append(tables.hhea.hhea(m).toTTX())

    log.out('[hmtx] ', 90, newline=False)
    root.append(tables.hmtx.hmtx(m, glyphs).toTTX())

    log.out('[vhea] ', 90, newline=False)
    root.append(tables.vhea.vhea(m).toTTX())

    log.out('[vmtx]', 90)
    root.append(tables.vmtx.vmtx(m, glyphs).toTTX())




    # glyph-code mappings
    # ---------------------------------------------

    # single glyphs
    log.out('[cmap] ', 90, newline=False)
    root.append(tables.cmap.toTTX(glyphs, flags["no_vs16"]))



    # ligatures
    ligatures = False

    # check for presence of ligatures
    for g in glyphs:
        if len(g) > 1:
            ligatures = True

    if ligatures:

        if formats[chosenFormat]["ligatureFormat"] == "OpenType":
            #log.out ('Assembling GDEF table...', 90)
            #root.append(tables.gdef.toTTX(glyphs))

            #log.out ('Assembling GPOS table...', 90)
            #root.append(tables.gpos.toTTX())

            log.out('[GSUB] ', 36, newline=False)
            root.append(tables.gsub.gsub(glyphs).toTTX())


        elif formats[chosenFormat]["ligatureFormat"] == "TrueType":
            log.out('[morx] ', 36, newline=False)
            root.append(tables.morx.toTTX(glyphs))




    # glyf
    # ---------------------------------------------

    # glyf is used as a placeholde to please font validation,
    # table dependencies and the TTX compiler.
    #
    # CBDT/CBLC doesn't use glyf at all
    if glyphFormat is not "CBx":
        log.out('[glyf] ', 36, newline=False)
        root.append(tables.glyf.toTTX(m, glyphs))


    # actual glyph picture data
    # ---------------------------------------------

    if glyphFormat == "SVG":
        log.out('[SVG ]', 36)
        root.append(tables.svg.svg(m, glyphs).toTTX())

    elif glyphFormat == "sbix":
        log.out('[sbix]', 36)
        root.append(tables.sbix.sbix(glyphs).toTTX())

    elif glyphFormat == "CBx":
        log.out('[CBLC] ', 36, newline=False)
        root.append(tables.cblc.cblc(m, glyphs).toTTX())

        log.out('[CBDT]', 36)
        root.append(tables.cbdt.cbdt(m, glyphs).toTTX())




    # human-readable metadata
    # ---------------------------------------------
    log.out('[name]', 90)
    root.append(tables.name.toTTX(chosenFormat, m))




    # the TTX is now done! (as long as something didn't go wrong)
    # return an XML string
    return tostring(root, pretty_print=True, method="xml", xml_declaration=True, encoding="UTF-8")

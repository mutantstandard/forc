from lxml.etree import Element, ElementTree, fromstring



def gdef(glyphs):

    gdef = Element("GDEF")

    gdef.append(Element("Version", {"value": "0x00010000"}))


    # GlyphClassDef
    gcd = Element("GlyphClassDef", {"Format": "2"})

    for g in glyphs:
        if g.codepoints[0] != 0: # filter out .notdef
            if len(g.codepoints) > 1: # if a ligature
                classNum = "2"
            else:
                classNum = "1"

            gcd.append(Element("ClassDef", {"glyph": g.name, "class": classNum}))

    gdef.append(gcd)



    # LigCaretList
    lcl = Element("LigCaretList")

    lcl.append(Element("Coverage", {"Format": "2"}))

    gdef.append(lcl)

    return gdef

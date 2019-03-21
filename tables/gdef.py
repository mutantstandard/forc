from lxml.etree import Element, ElementTree, fromstring



def create(glyphs):
    """
    Creates a basic GDEF table.
    """

    gdef = Element("GDEF")

    gdef.append(Element("Version", {"value": "0x00010000"}))


    # GlyphClassDef
    gcd = Element("GlyphClassDef", {"Format": "2"})

    for g in glyphs['img']:
        if g.codepoints.seq[0] != 0: # filter out .notdef
            if len(g.codepoints.seq) > 1: # if a ligature
                classNum = 2
            else:
                classNum = 1

            gcd.append(Element("ClassDef", {"glyph": g.codepoints.name(), "class": str(classNum)}))

    gdef.append(gcd)



    # LigCaretList
    lcl = Element("LigCaretList")

    lcl.append(Element("Coverage", {"Format": "2"}))

    gdef.append(lcl)

    return gdef

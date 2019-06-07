from lxml.etree import Element
from data import Tag


# OTLFeature
# -----------------------------
# Classes representing common OpenType Layout Lookup structures.
# (https://docs.microsoft.com/en-us/typography/opentype/spec/chapter2#features-and-lookups)



def singleGlyphName(g): # TODO: replace this with a more complex name system for glyph classes.
    """
    Takes the first codepoint of a ligature and returns a string of it's glyph name.
    """
    return f"u{g.codepoints.seq[0]:x}"


def glyphName(int): # TODO: replace this with a more complex name system for glyph classes.
    return f"u{int:x}"


class LookupType4:
    """
    Table somewhat representing a LookupType 4.
    (https://docs.microsoft.com/en-us/typography/opentype/spec/gsub#lookuptype-4-ligature-substitution-subtable)

    Generated from user input glyphs.
    """
    def __init__(self, glyphs):
        self.lookupType = 4
        self.lookupFlag = 0

        # creating a data structure that will work for LigatureSets.
        ligatureSubst = {}

        for g in glyphs['all']:
            if len(g.codepoints) > 1: # if a ligature

                # if the first glyph has already been represented,
                # append it
                if singleGlyphName(g) in ligatureSubst.keys():
                    ligatureSubst[singleGlyphName(g)].append(g)

                # if not, then make a new list with it
                # and then append it
                else:
                    ligatureSubst[singleGlyphName(g)] = []
                    ligatureSubst[singleGlyphName(g)].append(g)


        self.ligatureSubst = ligatureSubst


    def toTTX(self, index):
        lookup = Element("Lookup", {"index": str(index) })

        lookup.append(Element("LookupType", {"value": str(self.lookupType) }))
        lookup.append(Element("LookupFlag", {"value": str(self.lookupFlag) }))

        ligatureSubst = Element("LigatureSubst", {"index": "0", "format": "1" })



        for firstCodepoint, ligatureSet in self.ligatureSubst.items():

            # Ligature subtables MUST be ordered from the longest lists to the shortest.
            # Otherwise, the text client probably won't find them.
            ligatureSet.sort(key=len, reverse=True)

            ligatureSetTTX = Element("LigatureSet", {"glyph" : firstCodepoint})

            for g in ligatureSet:
                if g.alias:
                    glyphTarget = g.alias.name()
                else:
                    glyphTarget = g.name()

                components = ','.join(map(glyphName, g.codepoints.seq[1:]))

                ligatureSetTTX.append(Element("Ligature", {"components": components, "glyph": glyphTarget }))

            ligatureSubst.append(ligatureSetTTX)

        lookup.append(ligatureSubst)



        return lookup




class LookupList:
    def __init__(self, glyphs):
        self.lookups = [LookupType4(glyphs)]

    def toTTX(self):
        lookupList = Element("LookupList")

        for index, l in enumerate(self.lookups):
            lookupList.append(l.toTTX(index))

        return lookupList

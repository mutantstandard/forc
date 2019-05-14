from lxml.etree import Element, ElementTree, fromstring


def glyphName(int):
    return "u" + (hex(int)[2:])

def singleGlyphName(g):
    """
    Takes the first codepoint of a ligature and returns a string of it's glyph name.
    """
    return glyphName(g.codepoints.seq[0])


def toTTX(glyphs):
    """
    Generates and returns a TTX GSUB table with ligature data.
    """

    gsub = Element("GSUB")


    # constant information

    gsub.append(Element("Version", {"value": "0x00010000"})) # hard-coded

    # generating the ScriptList
    # all of the way this is is hardcoded for a reason.

    # DFLT means 'no script in particular'
    # ReqFeatureIndex value 65535 tells OpenType we don't need any Features in particular.
    gsub.append(fromstring("""
        <ScriptList>
          <ScriptRecord index="0">
            <ScriptTag value="DFLT"/>
            <Script>
              <DefaultLangSys>
                <ReqFeatureIndex value="65535"/>
                <FeatureIndex index="0" value="0"/>
              </DefaultLangSys>
            </Script>
          </ScriptRecord>
        </ScriptList>
    """))


    # generating the FeatureList
    # all of the way this is is hardcoded for a reason.

    # one feature record, with a tag 'ccmp' (Glyph Composition/Decomposition)

    # a feature with all of the lookup lists (in LookupList) we are going
    # to use to store ligature data.

    gsub.append(fromstring("""
        <FeatureList>
          <FeatureRecord index="0">
            <FeatureTag value="liga"/>
            <Feature>
                <LookupListIndex index="0" value="0"/>
            </Feature>
          </FeatureRecord>
        </FeatureList>
    """))


    # generating the LookupList

    lookupList = Element("LookupList")

    lookup = Element("Lookup", {"index": "0"})
    lookup.append(Element("LookupType", {"value": "4"})) # value 4 for ligature substitution
    lookup.append(Element("LookupFlag", {"value": "0"}))

    ligaturesubst = Element("LigatureSubst", {"index": "0", "format": "1"}) # hard-coded.




    # creating a data structure that will work for LigatureSets.
    ligatureList = {}

    for g in glyphs['all']:
        if len(g.codepoints) > 1: # if a ligature
            if singleGlyphName(g) in ligatureList.keys():
                ligatureList[singleGlyphName(g)].append(g)
            else:
                ligatureList[singleGlyphName(g)] = []
                ligatureList[singleGlyphName(g)].append(g)



    # generating ligature XML
    for id, ligatureSet in ligatureList.items():

        # Ligature subtables MUST be ordered from the longest lists to the shortest.
        # Otherwise, the text client probably won't find them.
        ligatureSet.sort(key=len, reverse=True)

        ligatureSetXML = Element("LigatureSet", {"glyph": id})

        for g in ligatureSet:
            if g.alias:
                glyphTarget = g.alias.name()
            else:
                glyphTarget = g.codepoints.name()

            components = ','.join(map(glyphName, g.codepoints.seq[1:]))

            ligatureSetXML.append(Element("Ligature", {"components": components, "glyph": glyphTarget}))

        ligaturesubst.append(ligatureSetXML)


    lookup.append(ligaturesubst)
    lookupList.append(lookup)
    gsub.append(lookupList)


    return gsub

from lxml.etree import Element, ElementTree, fromstring


def glyphName(int):
    return "u" + (hex(int)[2:])

def singleGlyphName(g):
    """
    Takes the first codepoint of a ligature and returns a string of it's glyph name.
    """
    return glyphName(g.codepoints[0])


def gsub(glyphs):
    """
    Generates and returns a GSUB table with ligature data.
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
            <FeatureTag value="ccmp"/>
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

    for g in glyphs:
        if len(g.codepoints) > 1: # if a ligature
            if singleGlyphName(g) in ligatureList.keys():
                ligatureList[singleGlyphName(g)].append(g)
            else:
                ligatureList[singleGlyphName(g)] = []
                ligatureList[singleGlyphName(g)].append(g)

    # generating ligature XML
    for id, ligatureSet in ligatureList.items():
        ligatureSetXML = Element("LigatureSet", {"glyph": id})

        for g in ligatureSet:
            components = ','.join(map(glyphName, g.codepoints[1:]))

            ligatureSetXML.append(Element("Ligature", {"components": components, "glyph": g.name}))

        ligaturesubst.append(ligatureSetXML)


    lookup.append(ligaturesubst)
    lookupList.append(lookup)
    gsub.append(lookupList)


    return gsub

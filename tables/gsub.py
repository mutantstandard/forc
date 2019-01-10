from lxml.etree import Element, ElementTree, parse

def gsub(glyphs):
    """
    Generates and returns a GSUB table with ligature data.
    """

    gsub = Element("GSUB")


    # constant information

    gsub.append(Element("Version", {"value": "0x00010000"})) # hard-coded


    # all of the way this is is hardcoded for a reason.
    gsub.append(parse("""
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


    # all of the way this is is hardcoded for a reason.
    gsub.append(parse("""
        <FeatureList>
          <FeatureRecord index="0">
            <FeatureTag value="ccmp"/>
            <Feature>
                <!--??????-->
            </Feature>
          </FeatureRecord>
        </FeatureList>
    """))




    #for ID, g in enumerate(glyphs):


    return glyfTable

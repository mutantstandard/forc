from lxml.etree import Element, ElementTree, fromstring



def gpos():
    """
    Generates and returns a GSUB table with ligature data.
    """

    gpos = Element("GPOS")


    # constant information

    gpos.append(Element("Version", {"value": "0x00010000"})) # hard-coded

    # generating the ScriptList
    # all of the way this is is hardcoded for a reason.

    # DFLT means 'no script in particular'
    # ReqFeatureIndex value 65535 tells OpenType we don't need any Features in particular.
    gpos.append(fromstring("""
        <ScriptList>
          <ScriptRecord index="0">
            <ScriptTag value="DFLT"/>
            <Script>
              <DefaultLangSys>
                <ReqFeatureIndex value="65535"/>
              </DefaultLangSys>
            </Script>
          </ScriptRecord>
        </ScriptList>
    """))


    # FeatureList
    # all of the way this is is hardcoded for a reason.

    gpos.append(fromstring("""
        <FeatureList>
        </FeatureList>
    """))

    # LookupList
    # all of the way this is is hardcoded for a reason.

    gpos.append(fromstring("""
        <LookupList>
        </LookupList>
    """))



    return gpos

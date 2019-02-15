from lxml.etree import Element, ElementTree, fromstring


def morphSubtable(index):
    morph = Element("MorphSubstable", {"index": index})

    return morph


def morphFeature(index, featureType, featureSetting, enableFlags, disableFlags):

    feature = Element("MorphFeature", {"index": index})
    feature.append(Element("FeatureType", {"value": featureType}))
    feature.append(Element("FeatureSetting", {"value": featureSetting}))
    feature.append(Element("EnableFlags", {"value": enableFlags}))
    feature.append(Element("DisableFlags", {"value": disableFlags}))

    return feature


def morx(glyphs):
    """
    Generates and returns a morx table with ligature data.
    """

    morx = Element("morx")

    # header stuff
    # (hardcoded)
    morx.append(Element("Version", {"value": "2"}))
    morx.append(Element("Reserved", {"value": "0"}))




    # metamorphosis chain
    # (we only get the one)
    morphChain = Element("MorphChain", {"index": "0"})

    # chain header
    morphChain.append(Element("DefaultFlags", {"value": "0x00000003"})) #default spec for subtables

    # feature array
    morphChain.append(morphFeature("0", "1", "0", "0x00000001", "0xFFFFFFFF"))
    morphChain.append(morphFeature("1", "1", "1", "0x00000000", "0xFFFFFFFE"))
    morphChain.append(morphFeature("2", "27", "2", "0x00000002", "0xFFFFFFFF"))
    morphChain.append(morphFeature("3", "27", "3", "0x00000000", "0xFFFFFFFD"))
    morphChain.append(morphFeature("4", "0", "1", "0x00000000", "0x00000000"))

    # metamorphosis subtables
    # morphChain.append(morphSubtable("0"))




    morx.append(morphChain)



    return morx

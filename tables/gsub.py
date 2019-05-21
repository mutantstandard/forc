from lxml.etree import Element, ElementTree, fromstring
from tables.support.otlScript import ScriptList, ScriptRecord, Script
from tables.support.otlFeature import FeatureList, FeatureRecord, Feature
from tables.support.otlLookup import LookupList, LookupType4



class gsub:

    def __init__(self, glyphs):
        # we're using version 1.0 here, which doesn't have a
        # featureVariations table, because we don't need it.

        self.TTXversion = "0x00010000" # TODO: remove this and replace with a mechanism to translate existing data to TTX.
        self.majorVersion = 1
        self.minorVersion = 0

        self.scriptList = ScriptList() # non-editable ScriptList
        self.featureList = FeatureList() # non-editable FeatureList
        self.lookupList = LookupList(glyphs) # non-editable LookupList


    def toTTX(self):
        gsub = Element("GSUB")
        gsub.append(Element("Version", {"value": self.TTXversion }))

        gsub.append(self.scriptList.toTTX())
        gsub.append(self.featureList.toTTX())
        gsub.append(self.lookupList.toTTX())

        return gsub

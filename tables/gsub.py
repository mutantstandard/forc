from lxml.etree import Element, ElementTree, fromstring

from tables.support.otlScript import ScriptList, ScriptRecord, Script
from tables.support.otlFeature import FeatureList, FeatureRecord, Feature
from tables.support.otlLookup import LookupList, LookupType4



class gsub:

    def __init__(self, glyphs):

        # we're using version 1.0 here, which doesn't have a
        # featureVariations table, because we don't need it.
        self.majorVersion = 1
        self.minorVersion = 0
        self.TTXversion = '0x00010000' # TODO: Convert in some way so it can dynamically reflect the official values.

        self.scriptList = ScriptList() # non-editable ScriptList
        self.featureList = FeatureList() # non-editable FeatureList
        self.lookupList = LookupList(glyphs) # non-editable LookupList




    def toTTX(self):
        gsub = Element("GSUB")
        gsub.append(Element("Version", {"value": str(self.TTXversion) }))

        gsub.append(self.scriptList.toTTX())
        gsub.append(self.featureList.toTTX())
        gsub.append(self.lookupList.toTTX())

        return gsub

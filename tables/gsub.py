import struct
from lxml.etree import Element, ElementTree, fromstring

from data import vFixed
from tables.support.otlScript import ScriptList, ScriptRecord, Script
from tables.support.otlFeature import FeatureList, FeatureRecord, Feature
from tables.support.otlLookup import LookupList, LookupType4



class gsub:

    def __init__(self, glyphs):

        # we're using version 1.0 here, which doesn't have a
        # featureVariations table, because we don't need it.
        self.majorVersion = 1
        self.minorVersion = 0

        self.scriptList = ScriptList() # non-editable ScriptList
        self.featureList = FeatureList() # non-editable FeatureList
        self.lookupList = LookupList(glyphs) # non-editable LookupList


    def toTTX(self):
        gsub = Element("GSUB")
        gsub.append(Element("Version", {"value": vFixed(f"{self.majorVersion}.{self.minorVersion}").toHexStr() })) # TTX wants the version in this format.

        gsub.append(self.scriptList.toTTX())
        gsub.append(self.featureList.toTTX())
        gsub.append(self.lookupList.toTTX())

        return gsub

    def toBytes(self):

        # TODO: make toBytes functions for OTL scripts, features and lookups.
        # TODO: learn how to generate offsets for OTL scripts, features and lookups.
        
        # - generate the scriptList, featureList, and lookup list, generate offsets.

        gsub = struct.pack( ">HH"
                          , self.majorVersion # UInt16
                          , self.minorVersion # UInt16

                          # offset to scriptList # Offset16
                          # offset to featureList # Offset16
                          # offset to lookupList # Offset16
                          )

        # - dump the lists immediately after this information
        # - return the table.

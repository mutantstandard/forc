from lxml.etree import Element
from data import tag


# OTLScript
# -----------------------------
# Classes representing common OpenType Layout Script structures.
# (https://docs.microsoft.com/en-us/typography/opentype/spec/chapter2#scripts-and-languages)



class Script:
    """
    Class representing a placeholder Script table.
    Currently not editable atm - it's just designed to have the right data for forc's particular context.
    """
    def __init(self):
        self.whatever = 0

    def toTTX(self):
        script = Element("Script")

        # ReqFeatureIndex value 65535 tells OpenType we don't need any Features in particular.
        dfl = Element("DefaultLangSys")
        dfl.append(Element("ReqFeatureIndex", {"value": "65535" }))
        dfl.append(Element("FeatureIndex", {"index": "0", "value": "0" }))

        script.append(dfl)

        return script



class ScriptRecord:
    """
    Class representing a placeholder ScriptRecord table.
    Currently not editable atm - it's just designed to have the right data for forc's particular context.
    """
    def __init__(self):

        self.scriptTag = tag("DFLT") # script tag identifier.
        # DFLT means 'no script in particular'

        self.script = Script() # placeholder script table.

    def toTTX(self, index):
        scriptRecord = Element("ScriptRecord", {"index": str(index) })
        scriptRecord.append(Element("ScriptTag", {"value": str(self.scriptTag) }))
        scriptRecord.append(self.script.toTTX())

        return scriptRecord



class ScriptList:
    """
    Class representing a ScriptList table.
    """
    def __init__(self):
        self.scriptRecords = [ScriptRecord()] # array of script tables.

    def toTTX(self):
        scriptList = Element("ScriptList")

        for index, sr in enumerate(self.scriptRecords):
            scriptList.append(sr.toTTX(index))

        return scriptList

from lxml.etree import Element, ElementTree, tostring, fromstring
import subprocess
import pathlib
from base64 import b64encode

import log





def addEntry(element, tag, text):
    """
    Creates a plist-style XML entry
    """
    entry = Element(tag)
    entry.text = text
    element.append(entry)





def compileiOSConfig(manifest, font, outputPath):
    """
    Takes a finished font and uses the manifest metadata to compile
    a valid iOS Configuration Profile with the font embedded.
    """

    m = manifest['metadata']['iOSConfig']

    root = Element('plist', {'version': '1.0'}) # hard-coded attrs.


    # Initial Dict
    # ------------------------------------------------

    dict = Element('dict')

    addEntry(dict, 'key', 'PayloadDisplayName')
    addEntry(dict, 'string', m['PayloadDisplayName'])

    addEntry(dict, 'key', 'PayloadIdentifier')
    addEntry(dict, 'string', m['PayloadIdentifier'])

    if "PayloadDescription" in m:
        addEntry(dict, 'key', 'PayloadDescription')
        addEntry(dict, 'string', m['PayloadDescription'])

    addEntry(dict, 'key', 'PayloadRemovalDisallowed')
    dict.append(Element('false')) # hard-coded

    addEntry(dict, 'key', 'PayloadType')
    addEntry(dict, 'string', 'Configuration') # hard-coded

    addEntry(dict, 'key', 'PayloadUUID')
    addEntry(dict, 'string', m['PayloadUUID'])

    addEntry(dict, 'key', 'PayloadVersion')
    addEntry(dict, 'integer', str(m['PayloadVersion']))

    addEntry(dict, 'key', 'PayloadContent')





    # PayloadContent
    # ------------------------------------------------

    contentArray = Element('array')

    contentDict = Element('dict')

    addEntry(contentDict, 'key', 'Name')
    addEntry(contentDict, 'string', m['ContentPayloadName'])

    addEntry(contentDict, 'key', 'PayloadIdentifier')
    addEntry(contentDict, 'string', m['ContentPayloadIdentifier'])

    addEntry(contentDict, 'key', 'PayloadType')
    addEntry(contentDict, 'string', 'com.apple.font')

    addEntry(contentDict, 'key', 'PayloadUUID')
    addEntry(contentDict, 'string', m['ContentPayloadUUID'])

    addEntry(contentDict, 'key', 'PayloadVersion')
    addEntry(contentDict, 'integer', str(m['ContentPayloadVersion']))

    addEntry(contentDict, 'key', 'Font')



    # Font
    # ------------------------------------------------
    with open(font, "rb") as read_file:
        encodedFont = b64encode(read_file.read())


    fontData = Element('data')
    fontData.text = encodedFont

    contentDict.append(fontData)


    # stitching it together
    # ------------------------------------------------

    contentArray.append(contentDict)
    dict.append(contentArray)
    root.append(dict)

    appleDoctype = """<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">"""

    return tostring(root, pretty_print=True, method="xml", xml_declaration=True, encoding="UTF-8", doctype=appleDoctype)

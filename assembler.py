from xml.etree.ElementTree import Element, tostring
from xml.dom import minidom

from tables.glyphOrder import glyphOrder
from tables.head import head
from tables.os2 import os2
from tables.post import post
from tables.name import name
from tables.maxp import maxp
from tables.horizontalMetrics import hhea, hmtx
from tables.verticalMetrics import vhea, vmtx
from tables.cmap import cmap



def assembler():

  xMin = -1024
  xMax = 1024

  yMin = -470
  yMax = 1578

  unitsPerEm = 2048
  lowestRecPPEM = 16

  created = "Mon Jan 03 13:45:00 2019"

  OS2ySubscriptXSize = 0
  OS2ySubscriptYSize = 0
  OS2ySubscriptXOffset = 0
  OS2ySubscriptYOffset = 0
  OS2ySuperscriptXSize = 0
  OS2ySuperscriptYSize = 0
  OS2ySuperscriptXOffset = 0
  OS2ySuperscriptYOffset = 0
  OS2yStrikeoutSize = 0
  OS2yStrikeoutPosition = 0



  OS2VendorID = "MTNT"

  macLangID = "0x0"
  msftLangID = "0x809"

  nameRecords =   {"0" : "Copyright ©2017-2019 Dzuk"
                  ,"1" : "Mutant Standard emoji (SVGinOT)"
                  ,"2" : "Regular"
                  ,"3" : "Mutant Standard emoji SVGinOT 0.3.1"
                  ,"4" : "Mutant Standard emoji (SVGinOT)"
                  ,"5" : "0.3.1 (3rd January 2019)"
                  ,"6" : "MutantStandard-SVGinOT-Regular"
                  ,"8" : "Mutant Standard"
                  ,"9" : "Dzuk"
                  ,"10" : "When using the special emoji within this font that aren't supported by Unicode, make sure you are not using them in situations where other people or devices may not have this font installed, or those who are visually impaired. See [URL] for more information."
                  ,"11" : "https://mutant.tech"
                  ,"12" : "https://noct.zone"
                  ,"13" : "Mutant Standard emoji is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License."
                  ,"14" : "https://creativecommons.org/licenses/by-nc-sa/4.0/"
                  ,"16" : "Mutant Standard emoji (SVGinOT)"
                  ,"17" : "Complete"
                  }






  # putting the TTX together

  root = Element('ttFont')
  root.attrib = {'sfntVersion': '\\x00\\x01\\x00\\x00', 'ttLibVersion': '3.28'} # hard-coded attrs.

  root.append(glyphOrder())
  root.append(head())
  root.append(os2())
  root.append(post())
  root.append(maxp())
  root.append(Element("loca")) # just to please macOS, it's supposed to be empty.

  root.append(hhea())
  root.append(hmtx())
  root.append(vhea())
  root.append(vmtx())

  root.append(cmap(macLangID, msftLangID))
  # GDEF, GSUB, etc.
  # glyf
  # SVG/sbix/CBDT+CBLC

  root.append(name(nameRecords, macLangID, msftLangID))








  # prettyyyy~~~~

  stringOutput = tostring(root, encoding="unicode", method="xml")
  reparsedXML = minidom.parseString(stringOutput)
  prettyOutput = reparsedXML.toprettyxml(indent="  ")


  return prettyOutput

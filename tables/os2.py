from xml.etree.ElementTree import Element

def os2():
    """
    Creates an OS/2 table and fills it with both hard-coded and
    user-defined metadata.
    """
    os2 = Element("OS_2")

    os2.append(Element("version", {'value': '5'})) # hard-coded

    os2.append(Element("xAvgCharWidth", {'value': '2048'})) # xMax
    os2.append(Element("usWeightClass", {'value': '500'})) # hard-coded?
    os2.append(Element("usWidthClass", {'value': '5'})) # hard-coded?

    os2.append(Element("fsType", {'value': '00000000 00000000'})) # hard-coded. must agree with head's macStyle


    os2.append(Element("ySubscriptXSize", {'value': '0'}))
    os2.append(Element("ySubscriptYSize", {'value': '0'}))
    os2.append(Element("ySubscriptXOffset", {'value': '0'}))
    os2.append(Element("ySubscriptYOffset", {'value': '0'}))

    os2.append(Element("ySuperscriptXSize", {'value': '0'}))
    os2.append(Element("ySuperscriptYSize", {'value': '0'}))
    os2.append(Element("ySuperscriptXOffset", {'value': '0'}))
    os2.append(Element("ySuperscriptYOffset", {'value': '0'}))

    os2.append(Element("yStrikeoutSize", {'value': '0'}))
    os2.append(Element("yStrikeoutPosition", {'value': '0'}))

    os2.append(Element("sFamilyClass", {'value': '5'})) # hard-coded

    # all panose elements are hard-coded
    panose = Element("panose")
    panose.append(Element("bFamilyType", {'value': "2"}))
    panose.append(Element("bSerifStyle", {'value': "0"}))
    panose.append(Element("bWeight", {'value': "6"}))
    panose.append(Element("bProportion", {'value': "9"}))
    panose.append(Element("bContrast", {'value': "0"}))
    panose.append(Element("bStrokeVariation", {'value': "0"}))
    panose.append(Element("bArmStyle", {'value': "0"}))
    panose.append(Element("bLetterForm", {'value': "0"}))
    panose.append(Element("bMidline", {'value': "0"}))
    panose.append(Element("bXHeight", {'value': "0"}))
    os2.append(panose)

    os2.append(Element("ulUnicodeRange1", {'value': '00000000 00000000 00000000 00000000'}))
    os2.append(Element("ulUnicodeRange2", {'value': '00000000 00000000 00000000 00000000'}))
    os2.append(Element("ulUnicodeRange3", {'value': '00000000 00000000 00000000 00000000'}))
    os2.append(Element("ulUnicodeRange4", {'value': '00000000 00000000 00000000 00000000'}))

    os2.append(Element("achVendID", {'value': ''}))

    os2.append(Element("fsSelection", {'value': '00000000 00000000'})) # hard-coded

    os2.append(Element("usFirstCharIndex", {'value': '0x0'}))
    os2.append(Element("usLastCharIndex", {'value': '0x0'}))

    os2.append(Element("sTypoAscender", {'value': '0'}))
    os2.append(Element("sTypoDescender", {'value': '0'}))
    os2.append(Element("sTypoLineGap", {'value': '0'}))
    os2.append(Element("usWinAscent", {'value': '0'}))
    os2.append(Element("usWinDescent", {'value': '0'}))

    os2.append(Element("ulCodePageRange1", {'value': '00000000 00000000 00000000 00000000'}))
    os2.append(Element("ulCodePageRange2", {'value': '00000000 00000000 00000000 00000000'}))

    os2.append(Element("sxHeight", {'value': '0'}))
    os2.append(Element("sCapHeight", {'value': '0'}))

    os2.append(Element("usDefaultChar", {'value': '0'}))
    os2.append(Element("usBreakChar", {'value': '0x20'}))
    os2.append(Element("usMaxContext", {'value': '1'}))

    os2.append(Element("usLowerOpticalPointSize", {'value': '0'}))
    os2.append(Element("usUpperOpticalPointSize", {'value': '0'}))


    return os2

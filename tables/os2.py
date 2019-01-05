from xml.etree.ElementTree import Element

def os2(metrics, OS2VendorID):
    """
    Creates an OS/2 table and fills it with both hard-coded and
    user-defined metadata.
    """


    os2 = Element("OS_2")

    os2.append(Element("version", {'value': '5'})) # hard-coded

    os2.append(Element("xAvgCharWidth", {'value': str(metrics['xMax']) })) # xMax
    os2.append(Element("usWeightClass", {'value': '500'})) # hard-coded?
    os2.append(Element("usWidthClass", {'value': '5'})) # hard-coded?

    os2.append(Element("fsType", {'value': '00000000 00000000'})) # hard-coded. must agree with head's macStyle





    os2.append(Element("ySubscriptXSize", {'value': str(metrics['OS2ySubscriptXSize']) }))
    os2.append(Element("ySubscriptYSize", {'value': str(metrics['OS2ySubscriptYSize']) }))
    os2.append(Element("ySubscriptXOffset", {'value': str(metrics['OS2ySubscriptXOffset']) }))
    os2.append(Element("ySubscriptYOffset", {'value': str(metrics['OS2ySubscriptYOffset']) }))

    os2.append(Element("ySuperscriptXSize", {'value': str(metrics['OS2ySuperscriptXSize']) }))
    os2.append(Element("ySuperscriptYSize", {'value': str(metrics['OS2ySuperscriptYSize']) }))
    os2.append(Element("ySuperscriptXOffset", {'value': str(metrics['OS2ySuperscriptXOffset']) }))
    os2.append(Element("ySuperscriptYOffset", {'value': str(metrics['OS2ySuperscriptYOffset']) }))

    os2.append(Element("yStrikeoutSize", {'value': str(metrics['OS2yStrikeoutSize']) }))
    os2.append(Element("yStrikeoutPosition", {'value': str(metrics['OS2yStrikeoutPosition']) }))




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

    os2.append(Element("achVendID", {'value': OS2VendorID}))

    os2.append(Element("fsSelection", {'value': '00000000 00000000'})) # hard-coded

    os2.append(Element("usFirstCharIndex", {'value': '0x0'}))
    os2.append(Element("usLastCharIndex", {'value': '0x0'}))

    os2.append(Element("sTypoAscender", {'value': str(metrics['yMax']) }))
    os2.append(Element("sTypoDescender", {'value': str(metrics['OS2WeirdDescent']) }))
    os2.append(Element("sTypoLineGap", {'value': str(metrics['lineGap']) }))
    os2.append(Element("usWinAscent", {'value': str(metrics['yMax']) }))
    os2.append(Element("usWinDescent", {'value': str(metrics['OS2WeirdDescent']) }))

    os2.append(Element("ulCodePageRange1", {'value': '00000000 00000000 00000000 00000000'}))
    os2.append(Element("ulCodePageRange2", {'value': '00000000 00000000 00000000 00000000'}))

    os2.append(Element("sxHeight", {'value': '0'})) # leaving it hard-coded at 0 for now.
    os2.append(Element("sCapHeight", {'value': str(metrics['yMax']) }))

    os2.append(Element("usDefaultChar", {'value': '0'}))
    os2.append(Element("usBreakChar", {'value': '0x20'}))
    os2.append(Element("usMaxContext", {'value': '1'}))

    os2.append(Element("usLowerOpticalPointSize", {'value': '0'}))
    os2.append(Element("usUpperOpticalPointSize", {'value': '0'}))


    return os2

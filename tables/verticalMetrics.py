from lxml.etree import Element

def vhea(metrics):

    vhea = Element("vhea")

    vhea.append(Element("tableVersion", {'value': '0x00010000'}))  # hard-coded

    vhea.append(Element("ascent", {'value': str(metrics['xMax']) }))
    vhea.append(Element("descent", {'value': str(metrics['xMin']) }))
    vhea.append(Element("lineGap", {'value': "0" })) # hard-coded based on best practices

    vhea.append(Element("advanceHeightMax", {'value': str(metrics['yMax']) }))
    vhea.append(Element("minTopSideBearing", {'value': str(metrics['xMin']) }))
    vhea.append(Element("minBottomSideBearing", {'value': str(metrics['xMax']) }))
    vhea.append(Element("yMaxExtent", {'value': '2048'}))

    vhea.append(Element("caretSlopeRise", {'value': '1'})) # probably hard-coded
    vhea.append(Element("caretSlopeRun", {'value': '0'})) # probably hard-coded
    vhea.append(Element("caretOffset", {'value': '0'})) # probably hard-coded

    ## yes, this is different from vhea. tables are weird.
    vhea.append(Element("reserved1", {'value': '0'})) # hard-coded
    vhea.append(Element("reserved2", {'value': '0'})) # hard-coded
    vhea.append(Element("reserved3", {'value': '0'})) # hard-coded
    vhea.append(Element("reserved4", {'value': '0'})) # hard-coded

    vhea.append(Element("metricDataFormat", {'value': '0'})) # hard-coded
    vhea.append(Element("numberOfHMetrics", {'value': '0'})) # maybe TTX auto-denerates this?

    return vhea


def vmtx(metrics, glyphs):

    vmtx = Element("vmtx")

    for g in glyphs:
        if g.name is 'space':
            vmtx.append(Element("mtx",  {"name": g.name
                                        ,"height": str(metrics['spaceVLength'])
                                        ,"tsb": str(metrics['normalTSB'])
                                        }))
        elif g.name is 'CR':
            vmtx.append(Element("mtx", {"name": g.name
                                        ,"height": "0"
                                        ,"tsb": "0"
                                        }))
        else:
            vmtx.append(Element("mtx", {"name": g.name
                                        ,"height": str(metrics['normalHeight'])
                                        ,"tsb": str(metrics['normalTSB'])
                                        }))

    return vmtx

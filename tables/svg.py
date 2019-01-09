import lxml.etree as etree
from io import BytesIO

def strip_ns_prefix(tree):
    #iterate through only element nodes (skip comment node, text node, etc) :
    for element in tree.xpath('descendant-or-self::*'):
        #if element has prefix...
        if element.prefix:
            #replace element name with its local name
            element.tag = etree.QName(element).localname
    return tree



def svg(metrics, glyphs):
    """
    Generates and returns a SVG table.

    It will non-destructively alter glyphs or throw exceptions if there's visual data
    that's incompatible with SVGinOT standards and/or renderers.
    """

    svgTable = etree.Element("SVG")

    for ID, g in enumerate(glyphs):
        if g.imagePath:
            svgDoc = etree.Element("svgDoc", {"startGlyphID": str(ID), "endGlyphID" : str(ID) })

            # lxml can't parse from Path objects, so it has to give a string representation.
            svgET = etree.parse(g.imagePath.as_uri())
            svgImage = svgET.getroot()


            # we have to see if there's a viewBox and if there is, remove it and use
            # transforms to rectify the image's metrics.
            #
            # (viewBox is technically supported but behaves erratically in
            # most SVGinOT renderers)

            cdata = etree.CDATA("")

            if svgImage.find(".[@viewBox]"):

                # calculate the transform
                viewBoxWidth = svgImage.attrib['viewBox'].split(' ')[2] # get the 3rd viewBox number (width)

                xPos = str(metrics['xMin'])
                yPos = str(-(metrics['yMax'])) # negate and make into a string
                scale = metrics['unitsPerEm'] / int(viewBoxWidth) # determine the scale for the glyph based on UPEM.


                # make a transform group to wrap the SVG contents around
                transformGroup = etree.Element("g", {"transform": f"translate({xPos}, {yPos}) scale({scale})"})

                for tag in iter(svgImage):
                    transformGroup.append(tag)


                # make a new SVG tag without the viewbox and append the transform group to it.
                svgcdataPre = etree.Element(svgImage.tag, svgImage.attrib)
                svgcdataPre.attrib.pop("viewBox")
                etree.cleanup_namespaces(svgcdataPre)
                svgcdataPre.append(transformGroup)


                # because lxml has a thing for annoying namespaces, you've gotta strip those out
                svgCdataRoot = svgcdataPre.getroottree()
                strip_ns_prefix(svgCdataRoot)
                svgCdata = svgCdataRoot.getroot()


                # now you can finally make it the CDATA.
                cdata = etree.CDATA(etree.tostring(svgCdata, method="xml", pretty_print="true"))

            else:
                cdata = etree.CDATA("")


            svgDoc.text = cdata
            svgTable.append(svgDoc)






            # Throw an error if there's a style attribute, because
            # they're not compatible.
            #
            # I don't think it's this software's place to deal with
            # this, so it's gonna throw an exception instead.

            if svgImage.find(".[@style]"):
                raise Exception(f"SVG image {g.imagePath} has a 'style' attribute. These are not compatible in SVGinOT fonts.")

    return svgTable

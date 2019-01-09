import lxml.etree as etree
from io import BytesIO

def strip_ns_prefix(tree):
    #xpath query for selecting all element nodes in namespace
    query = "descendant-or-self::*[namespace-uri()!='']"
    #for each element returned by the above xpath query...
    for element in tree.xpath(query):
        #replace element name with its local name
        element.tag = etree.QName(element).localname

    etree.cleanup_namespaces(tree)

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
                svgcdata = etree.Element(svgImage.tag, svgImage.attrib)
                svgcdata.attrib.pop("viewBox")
                etree.cleanup_namespaces(svgcdata)
                svgcdata.append(transformGroup)


                # because lxml has a thing for annoying namespaces, you've gotta strip those out
                svgcdatatree = svgcdata.getroottree()
                strip_ns_prefix(svgcdatatree)

                # now you can finally make it the CDATA.
                cdata = etree.CDATA(etree.tostring(svgcdata, method="xml", pretty_print=False))

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

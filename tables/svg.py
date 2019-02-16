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




def stripStyles(svgImage):
    elements = svgImage.findall(f"//*[@style]")

    for e in elements:
        styleString = e.attrib['style']
        styleListPre = styleString.split(";")

        for style in styleListPre:
            splitStyle = style.split(":")

            e.attrib[splitStyle[0]] = splitStyle[1]

        e.attrib.pop("style")




def viewboxCompensate(metrics, svgTree, ID):
    """
    Strips out the viewBox attribute of an SVG and transforms it using metrics
    determined in the manifest to compensate for the loss of the viewBox.
    """

    svgImage = svgTree.getroot()

    # calculate the transform
    # ---------------------------------------------------------------------------
    viewBoxWidth = svgImage.attrib['viewBox'].split(' ')[2] # get the 3rd viewBox number (width)

    xPos = str(metrics['xMin'])
    yPos = str(-(metrics['yMax'])) # negate and make into a string
    scale = metrics['unitsPerEm'] / int(viewBoxWidth) # determine the scale for the glyph based on UPEM.



    # make a transform group to wrap the SVG contents around
    # ---------------------------------------------------------------------------
    transformGroup = etree.Element("g", {"transform": f"translate({xPos}, {yPos}) scale({scale})"})

    for tag in iter(svgImage):
        transformGroup.append(tag)



    # make a new SVG tag without the viewbox and append the transform group to it.
    # ---------------------------------------------------------------------------
    svgcdata = etree.Element(svgImage.tag, svgImage.attrib)
    svgcdata.attrib.pop("viewBox")
    etree.cleanup_namespaces(svgcdata)
    svgcdata.append(transformGroup)



    # because lxml has a thing for annoying namespaces, you've gotta strip those out
    # ---------------------------------------------------------------------------
    svgcdatatree = svgcdata.getroottree()
    strip_ns_prefix(svgcdatatree)


    return svgcdatatree





def svgAttrNormalisation(svgTree, ID):
    """
    Adds necessary attributes to the SVG XML for the SVG to render in text clients.
    """
    svg = svgTree.getroot()

    svg.attrib["id"] = f"glyph{ID}"
    svg.attrib["xmlns"] = "http://www.w3.org/2000/svg"
    svg.attrib["xlink"] = "http://www.w3.org/1999/xlink"

    newSVGTree = svg.getroottree()

    return newSVGTree




def svg(metrics, glyphs):
    """
    Generates and returns a SVG table.

    It will non-destructively alter glyphs or throw exceptions if there's visual data
    that's incompatible with SVGinOT standards and/or renderers.
    """

    svgTable = etree.Element("SVG")

    NAMESPACE = '{http://www.w3.org/2000/svg}'

    for ID, g in enumerate(glyphs):
        if g.imagePath:
            if g.imagePath['svg']:
                svgDoc = etree.Element("svgDoc", {"startGlyphID": str(ID), "endGlyphID" : str(ID) })

                # lxml can't parse from Path objects, so it has to give a string representation.
                svgImage = etree.parse(g.imagePath['svg'].as_uri())


                # we have to see if there's a viewBox and if there is, remove it and use
                # transforms to rectify the image's metrics.
                #
                # (viewBox is technically supported but behaves erratically in
                # most SVGinOT renderers)

                cdata = etree.CDATA("")


                # Throw an error if any of these elements are present.
                # -------------------------------------------------------------------------------------

                restrictedElements = [ 'text'
                                     , 'font'
                                     , 'foreignObject'
                                     , 'switch'
                                     , 'script'
                                     , 'a'
                                     , 'view'
                                     ]

                notRequiredElements = [ 'filter'
                                      , 'pattern'
                                      , 'mask'
                                      , 'marker'
                                      , 'symbol'
                                      , 'style'
                                      , 'cursor'
                                      ]


                for elem in restrictedElements:
                    if svgImage.find('//*' + NAMESPACE + elem) is not None:
                        raise Exception(f"SVG image {g.imagePath} has a {elem} element. These are not compatible in SVGinOT fonts.")

                for elem in notRequiredElements:
                    if svgImage.find('//*' + NAMESPACE + elem) is not None:
                        log.out(f"SVG image {g.imagePath} has a {elem} element. Compatibility with this is not mandatory.", 31)

                #if svgImage.find(f"//*[@style]") is not None:
                    #stripStyles(svgImage)
                    #raise Exception(f"SVG image {g.imagePath} has a 'style' attribute. These are not compatible in SVGinOT fonts.")


                finishedSVG = etree.ElementTree(etree.Element("svg"))




                # check if there's a viewBox and compensate for it if that's the case.
                # if not, just pass it on.
                # -------------------------------------------------------------------------------------
                if svgImage.find(".[@viewBox]") is not None:
                    compensated = viewboxCompensate(metrics, svgImage, ID)
                    finishedSVG = svgAttrNormalisation(compensated, ID)

                else:
                    finishedSVG = svgAttrNormalisation(svgImage, ID)


                cdata = etree.CDATA(etree.tostring(finishedSVG, method="xml", pretty_print=False, xml_declaration=True, encoding="UTF-8"))

                svgDoc.text = cdata
                svgTable.append(svgDoc)





    return svgTable

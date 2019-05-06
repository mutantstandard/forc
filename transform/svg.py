import lxml.etree as etree
import lxml.builder as builder

def stripStyles(svgImage):
    """
    Converts all instances of CSS style attibutes in an SVG to basic XML attributes.
    """
    elements = svgImage.findall(f"//*[@style]")

    for e in elements:
        styleString = e.attrib['style']
        styleListPre = styleString.split(";")

        for style in styleListPre:
            if style: # if it's not blank because splits can generate blank ends if there's only one style.
                splitStyle = style.split(":")
                #print(splitStyle)

                e.attrib[splitStyle[0]] = splitStyle[1]

        e.attrib.pop("style")




def affinityDesignerCompensate(svgImage):
    """
    Compensates for shortcomings in Affinity's SVG exporter, whereby certain shapes
    (that are supposed to be filled black) are not given explicit fills or strokes.

    This causes certain shapes, when put in an SVG font, to take on the colour of the
    text around it.

    This function looks for paths and rects that have no fill and stroke, and gives
    them a black fill and stroke.
    """
    xmlns = "{http://www.w3.org/2000/svg}"

    pathXP = "//" + xmlns + "path"
    rectXP = "//" + xmlns + "rect"
    circleXP = "//" + xmlns + "circle"
    ellipseXP = "//" + xmlns + "ellipse"

    serifRect = svgImage.find("//{http://www.w3.org/2000/svg}rect[@id]")
    if serifRect is not None:
        serifRect.getparent().remove(serifRect)

    if svgImage.find(pathXP) is not None:
        for e in svgImage.findall(pathXP):
            if "fill" not in e.attrib and "stroke" not in e.attrib:
                e.attrib["fill"] = "#000000"

    if svgImage.find(rectXP) is not None:
        for e in svgImage.findall(rectXP):
            if "fill" not in e.attrib and "stroke" not in e.attrib:
                e.attrib["fill"] = "#000000"

    if svgImage.find(circleXP) is not None:
        for e in svgImage.findall(circleXP):
            if "fill" not in e.attrib and "stroke" not in e.attrib:
                e.attrib["fill"] = "#000000"

    if svgImage.find(ellipseXP) is not None:
        for e in svgImage.findall(ellipseXP):
            if "fill" not in e.attrib and "stroke" not in e.attrib:
                e.attrib["fill"] = "#000000"




def viewboxCompensate(metrics, svgImage):
    """
    viewboxes in SVGinOT are poorly and inconsistently implemented among many vendors,
    leading to serious font display issuies.

    This function strips out the viewBox attribute of an SVG and transforms it using metrics
    determined in the manifest to compensate for the loss of the viewBox.
    """

    svgRoot = svgImage.getroot()

    # calculate the transform
    # ---------------------------------------------------------------------------
    viewBoxWidth = svgRoot.attrib['viewBox'].split(' ')[2] # get the 3rd viewBox number (width)

    xPos = str(metrics['xMin'])
    yPos = str(-(metrics['yMax'])) # negate
    scale = metrics['unitsPerEm'] / int(viewBoxWidth) # determine the scale for the glyph based on UPEM.



    # make a transform group to wrap the SVG contents around
    # ---------------------------------------------------------------------------
    transformGroup = etree.Element("g", {"transform": f"translate({xPos}, {yPos}) scale({scale})"})

    for tag in iter(svgRoot):
        transformGroup.append(tag)



    # make a new SVG tag without the viewbox and append the transform group to it.
    # ---------------------------------------------------------------------------
    nsmap = { None: "http://www.w3.org/2000/svg"
            , "xlink" : "http://www.w3.org/1999/xlink"
            }
    svgcdata = etree.Element(svgRoot.tag, svgRoot.attrib, nsmap = nsmap)
    svgcdata.attrib.pop("viewBox")
    svgcdata.attrib["version"] = "1.1"
    svgcdata.append(transformGroup)



    # because lxml has a thing for annoying namespaces, you've gotta strip those out
    # ---------------------------------------------------------------------------
    svgcdatatree = svgcdata.getroottree()

    return svgcdatatree


def compensateSVG(svgImage, m, afsc):

    metrics = m['metrics']

    # strip styles if there are any.
    if svgImage.find(f"//*[@style]") is not None:
        stripStyles(svgImage)

    if afsc:
        affinityDesignerCompensate(svgImage)

    if svgImage.find(".[@viewBox]") is not None:
        return viewboxCompensate(metrics, svgImage)
    else:
        return svgImage

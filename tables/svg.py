import lxml.etree as etree
import lxml.builder as builder
from io import BytesIO



def stripStyles(svgImage):
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
    Looks for paths and rects that have no fill and stroke, and gives them a black fill and stroke
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
    yPos = str(-(metrics['yMax'])) # negate
    scale = metrics['unitsPerEm'] / int(viewBoxWidth) # determine the scale for the glyph based on UPEM.



    # make a transform group to wrap the SVG contents around
    # ---------------------------------------------------------------------------
    transformGroup = etree.Element("g", {"transform": f"translate({xPos}, {yPos}) scale({scale})"})

    for tag in iter(svgImage):
        transformGroup.append(tag)



    # make a new SVG tag without the viewbox and append the transform group to it.
    # ---------------------------------------------------------------------------
    nsmap = { None: "http://www.w3.org/2000/svg"
            , "xlink" : "http://www.w3.org/1999/xlink"
            }
    svgcdata = etree.Element(svgImage.tag, svgImage.attrib, nsmap = nsmap)
    svgcdata.attrib.pop("viewBox")
    svgcdata.attrib["version"] = "1.1"
    svgcdata.append(transformGroup)



    # because lxml has a thing for annoying namespaces, you've gotta strip those out
    # ---------------------------------------------------------------------------
    svgcdatatree = svgcdata.getroottree()


    return svgcdatatree





def addGlyphID(svgTree, ID):
    """
    Adds the glyph ID to the SVG.
    """
    svg = svgTree.getroot()


    svg.attrib["id"] = f"glyph{ID}"
    newSVGTree = svg.getroottree()

    return newSVGTree




def create(m, glyphs, afsc):
    """
    Generates and returns a SVG table.

    It will non-destructively alter glyphs or throw exceptions if there's visual data
    that's incompatible with SVGinOT standards and/or renderers.
    """

    metrics = m['metrics']

    svgTable = etree.Element("SVG")

    for ID, g in enumerate(glyphs['img']):
        if g.imagePath and g.imagePath['svg']:
            svgDoc = etree.Element("svgDoc", {"startGlyphID": str(ID), "endGlyphID" : str(ID) })

            # lxml can't parse from Path objects, so it has to give a string representation.
            svgImage = etree.parse(g.imagePath['svg'].path.as_uri())


            cdata = etree.CDATA("")

            # strip styles if there are any.
            if svgImage.find(f"//*[@style]") is not None:
                stripStyles(svgImage)

            if afsc:
                affinityDesignerCompensate(svgImage)

            finishedSVG = etree.ElementTree(etree.Element("svg"))

            # check if there's a viewBox and compensate for it if that's the case.
            # if not, just pass it on.
            # -------------------------------------------------------------------------------------
            if svgImage.find(".[@viewBox]") is not None:
                compensated = viewboxCompensate(metrics, svgImage, ID)
                finishedSVG = addGlyphID(compensated, ID)

            else:
                finishedSVG = addGlyphID(svgImage, ID)


            cdata = etree.CDATA(etree.tostring(finishedSVG, method="xml", pretty_print=False, xml_declaration=True, encoding="UTF-8"))

            svgDoc.text = cdata
            svgTable.append(svgDoc)





    return svgTable

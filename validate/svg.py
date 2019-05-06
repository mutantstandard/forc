import lxml.etree as etree
import lxml.builder as builder
from io import BytesIO

import log



restrictedElems =    [ "a"
                     , "color-profile"
                     , "font"
                     , "icccolor"
                     , "switch"
                     , "script"
                     , "text"
                     , "view"
                     ]

restrictedAttrs = [ "contentStyleType"
                  , "color-profile"
                  ]



unenforcedElems = [ "animateTransform"
                  , "cursor"
                  , "filter"
                  , "marker"
                  , "mask"
                  , "pattern"
                  , "style"


                  # SVG Filter elements
                  , "feBlend"
                  , "feColorMatrix"
                  , "feComponentTransfer"
                  , "feComposite"
                  , "feConvolveMatrix"
                  , "feDiffuseLighting"
                  , "feDisplacementMap"
                  , "feDistantLight"
                  , "feDropShadow"
                  , "feGaussianBlur"
                  , "feImage"
                  , "feMerge"
                  , "feMergeNode"
                  , "feMorphology"
                  , "feOffset"
                  , "fePointLight"
                  , "feSpecularLighting"
                  , "feSpotLight"
                  , "feTile"
                  , "feTurbulence"
                  ]



unenforcedAttrs =   [ "cursor"
                    #, "style"
                    # -- style is compensated for in forc, so it's currently left out.
                    , "zoomAndPan"

                    # SVG event attributes
                    , "onbegin"
                    , "onend"
                    , "onrepeat"

                    , "onabort"
                    , "onerror"
                    , "onresize"
                    , "onscroll"
                    , "onunload"

                    , "oncopy"
                    , "oncut"
                    , "onpaste"

                    , "oncancel"
                    , "oncanplay"
                    , "oncanplaythrough"
                    , "onchange"
                    , "onclick"
                    , "onclose"
                    , "oncuechange"
                    , "ondblclick"
                    , "ondrag"
                    , "ondragend"
                    , "ondragenter"
                    , "ondragexit"
                    , "ondragleave"
                    , "ondragover"
                    , "ondragstart"
                    , "ondrop"
                    , "ondurationchange"
                    , "onemptied"
                    , "onended"
                    , "onerror"
                    , "onfocus"
                    , "oninput"
                    , "oninvalid"
                    , "onkeydown"
                    , "onkeypress"
                    , "onkeyup"
                    , "onload"
                    , "onloadeddata"
                    , "onloadedmetadata"
                    , "onloadstart"
                    , "onmousedown"
                    , "onmouseenter"
                    , "onmouseleave"
                    , "onmousemove"
                    , "onmouseout"
                    , "onmouseover"
                    , "onmouseup"
                    , "onmousewheel"
                    , "onpause"
                    , "onplay"
                    , "onplaying"
                    , "onprogress"
                    , "onratechange"
                    , "onreset"
                    , "onresize"
                    , "onscroll"
                    , "onseeked"
                    , "onseeking"
                    , "onselect"
                    , "onshow"
                    , "onstalled"
                    , "onsubmit"
                    , "onsuspend"
                    , "ontimeupdate"
                    , "ontoggle"
                    , "onvolumechange"
                    , "onwaiting"

                    , "onactivate"
                    , "onfocusin"
                    , "onfocusout"

                    ]


xmlns = '{http://www.w3.org/2000/svg}'
xlinkNS = '{http://www.w3.org/1999/xlink}'



def isSVGValid(path, ignoreUnenforcedContents=False):
    """
    Evaluates if a glyphs' SVG file is compliant with the SVGinOT standard.
    This checks for most things.

    Checks that currently don't exist:
    - relative units (em, ex, etc.)
    - rgba() colors
    - CSS2 color values in styles
    - XML entities

    """

    # these are both the same for historical reasons. They might change in the future.
    svgImagePath = path
    svgImageName = path

    svgImage = etree.parse(svgImagePath.as_uri())


    svgEmbeddedImages = svgImage.findall("//" + xmlns + "image")





    # Stuff relating to the root tag
    # --------------------------------------------------------------------

    # There must be an xmlns and it must be set to 'http://www.w3.org/2000/svg'.
    if None in svgImage.getroot().nsmap:
        if svgImage.getroot().nsmap[None] != 'http://www.w3.org/2000/svg':
            raise Exception(f"The SVG image '{svgImageName}' has a root namespace that is '{svgImage.getroot().nsmap[None]}'. It needs to be set to 'http://www.w3.org/2000/svg'.")
    else:
        raise Exception(f"The SVG image '{svgImageName}' doesn't have a root namespace. It needs one, and it needs to be set to 'http://www.w3.org/2000/svg'.")


    # If there is an xlink namespace, it must be set to "http://www.w3.org/1999/xlink".
    if "xlink" in svgImage.getroot().nsmap:
        if svgImage.getroot().nsmap["xlink"] != "http://www.w3.org/1999/xlink":
            raise Exception(f"The SVG image '{svgImageName}' has an xlink namespace that is '{svgImage.getroot().nsmap['xlink']}'. It needs to be set to 'http://www.w3.org/1999/xlink'.")


    # SVG version must either be "1.1" or unmarked.
    if "version" in svgImage.getroot().attrib:
        svgImageVersion = svgImage.getroot().attrib["version"]
        if not svgImageVersion == "1.1":
            raise Exception(f"The version of the SVG image '{svgImageName}' is set to '{svgImageVersion}'. It needs to either be set to 1.1 or removed entirely.")








    # Restricted contents
    # --------------------------------------------------------------------
    # These are explicitly not in the spec and should be disallowed under all circumstances.

    # elements
    for elem in restrictedElems:
        if svgImage.find('//' + xmlns + elem) is not None:
            raise Exception(f"The SVG image '{svgImageName}' has a '{elem}' element. These are not compatible in SVGinOT fonts.")

    # attributes
    for attr in restrictedAttrs:
        if svgImage.find(f"//*[@{attr}]") is not None:
            raise Exception(f"The SVG image '{svgImageName}' has a '{attr}' attribute. These are not compatible in SVGinOT fonts.")

    # image elements that contain SVGs
    if svgEmbeddedImages:
        for i in svgEmbeddedImages:
            href = i.attrib[xlinkNS + 'href']

            if href:
                if href.endswith('.svg'):
                    raise Exception(f"The SVG image '{svgImageName}' has an 'image' attribute that links to an SVG file. These are not compatible in SVGinOT fonts.")


    # XSL processing instructions exist in the file
    if "xsl" in svgImage.getroot().nsmap:
        raise Exception(f"The SVG image '{svgImageName}' contains XSL. This is not compatible in SVGinOT fonts.")


    # not included:
    #   - relative units (em, ex, etc.)
    #   - rgba() colors
    #   - CSS2 color values in styles





    # Unenforced Contents
    # --------------------------------------------------------------------
    # These are not enforced in the spec and are
    # not guaranteed to work.

    if not ignoreUnenforcedContents:

        # elements
        for elem in unenforcedElems:
            if svgImage.find('//' + xmlns + elem) is not None:
                raise Exception(f"The SVG image '{svgImageName}' has a '{elem}' element. Compatibility with this is not mandatory in SVGinOT fonts so it is not recommended.")

        # attributes
        for attr in unenforcedAttrs:
            if svgImage.find(f"//*[@{attr}]") is not None:
                raise Exception(f"The SVG image '{svgImageName}' has a '{attr}' attribute. Compatibility with this is not mandatory in SVGinOT fonts so it is not recommended.")


        # image elements that don't contain JPEGs or PNGs
        acceptedImageExtensions = ['.png', '.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi']

        if svgEmbeddedImages:
            for i in svgEmbeddedImages:
                href = i.attrib[xlinkNS + 'href']

                if href:
                    count = 0

                    for ext in acceptedImageExtensions:
                        if not href.endswith(ext):
                            count += 1

                    if count == len(acceptedImageExtensions):
                        raise Exception(f"The SVG image '{svgImageName}' has an image attribute that links to a file that is not a JPEG or PNG image. Compatibility with any image type other than PNG or JPEG is not mandatory in SVGinOT fonts so it is not recommended.")


        # there should be no SVG child elements.
        if svgImage.find("//{*}svg") is not None:
            raise Exception(f"The SVG image '{svgImageName}' has a child svg attribute. Compatibility with this is not mandatory in SVGinOT fonts so it is not recommended.")



        # not included:
        #   - XML entities

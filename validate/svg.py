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
                  , "svg"


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
                    #, "style" -- style is omitted here because it /can/ be compensated for.
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







def isSVGValid(g):
    svgImagePath = g.imagePath['svg']
    svgImageName = svgImagePath.name

    svgImage = etree.parse(svgImagePath.as_uri())

    NAMESPACE = '{http://www.w3.org/2000/svg}'



    # REALLY BASIC STUFF
    # --------------------------------------------------------------------

    # The xmlns is 'http://www.w3.org/2000/svg'.
    # xlink attribute is in the xmlns namespace.
    # xlink attribute is 'http://www.w3.org/1999/xlink'
    # SVG version is 1.1 or unmarked.






    # RESTRICTED CONTENTS
    # --------------------------------------------------------------------
    # These are explicitly not in the spec and should be disallowed under all circumstances.

    #print('----restricted----')
    for elem in restrictedElems:
        if svgImage.find('//*' + NAMESPACE + elem) is not None:
            raise Exception(f"The SVG image '{svgImageName}' has a '{elem}' element. These are not compatible in SVGinOT fonts.")


    for attr in restrictedAttrs:
        if svgImage.find(f"//*[@{attr}]") is not None:
            raise Exception(f"The SVG image '{svgImageName}' has a '{attr}' attribute. These are not compatible in SVGinOT fonts.")


    # TODO: measurements:
    #   - relative units (em, ex, etc.)
    #   - rgba() colors
    #   - CSS2 color values

    # TODO: image elements that contain SVG data.

    # TODO: XSL processing (???)








    # UNENFORCED CONTENTS
    # --------------------------------------------------------------------
    # These are not enforced in the spec and are
    # not guaranteed to work.


    #print('----unenforced----')
    for elem in unenforcedElems:
        if svgImage.find('//*' + NAMESPACE + elem) is not None:
            raise Exception(f"The SVG image '{svgImageName}' has a '{elem}' element. Compatibility with this is not mandatory in SVGinOT fonts so it is not recommended.")


    for attr in unenforcedAttrs:
        if svgImage.find(f"//*[@{attr}]") is not None:
            raise Exception(f"The SVG image '{svgImageName}' has a '{attr}' attribute. Compatibility with this is not mandatory in SVGinOT fonts so it is not recommended.")

    # TODO: image elements that don"t contain JPEGs or PNGs

    # TODO: XML entities (???)

    # any svg child elements (Xpath: "/svg/svg" TEST IF THIS WORKS)

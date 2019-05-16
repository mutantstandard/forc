from lxml.etree import Element

def toTTX(glyphs):
    post = Element("post")

    post.append(Element("formatType", {'value': '2.0'})) # hard-coded, Apple suggests against using formats 2.5, 3 and 4.
    post.append(Element("italicAngle", {'value': '0.0'})) # hard-coded

    post.append(Element("underlinePosition", {'value': '0'}))
    post.append(Element("underlineThickness", {'value': '0'}))

    post.append(Element("isFixedPitch", {'value': '1'})) # hard-coded

    post.append(Element("minMemType42", {'value': '0'})) # hard-coded
    post.append(Element("maxMemType42", {'value': '0'})) # hard-coded
    post.append(Element("minMemType1", {'value': '1'})) # hard-coded
    post.append(Element("maxMemType1", {'value': '1'})) # hard-coded

    post.append(Element("psNames"))


    # extraNames to please macOS.
    extraNames = Element("extraNames")
    for g in glyphs["img_empty"]:
        extraNames.append(Element("psName", {"name": g.name() }))

    post.append(extraNames)

    return post

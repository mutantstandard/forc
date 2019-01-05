from xml.etree.ElementTree import Element

def post(glyphs):
    post = Element("post")

    post.append(Element("formatType", {'value': '3.0'})) # hard-coded
    post.append(Element("italicAngle", {'value': '0.0'})) # hard-coded

    post.append(Element("underlinePosition", {'value': '0'}))
    post.append(Element("underlineThickness", {'value': '0'}))

    post.append(Element("isFixedPitch", {'value': '1'})) # hard-coded - this is monospaced

    post.append(Element("minMemType42", {'value': '0'})) # hard-coded
    post.append(Element("maxMemType42", {'value': '0'})) # hard-coded
    post.append(Element("minMemType1", {'value': '1'})) # hard-coded
    post.append(Element("maxMemType1", {'value': '1'})) # hard-coded

    post.append(Element("psNames"))


    # extraNames to please macOS.
    extraNames = Element("extraNames")
    for g in glyphs:
        extraNames.append(Element("psName", {"name": g.name}))

    post.append(extraNames)

    return post

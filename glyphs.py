import pathlib

import log



def glyphName(int):
    return (hex(int)[2:])


class glyph:

    def __init__(self, codepoints, name, imagePath=None, vs16=False):

        if codepoints:
            self.codepoints = codepoints
        elif imagePath:
            self.codepoints = [int(hex, 16) for hex in imagePath.stem.split(delim)]
        else:
            raise ValueError(f"Tried to make glyph object '{name}' but doesn't have a codepoint AND it doesn't have an image path.")

        if name:
            self.name = name
        else:
            self.name = 'u' + '_'.join(map(glyphName, codepoints))

        self.imagePath = imagePath
        self.vs16 = vs16




    def __str__(self):
        return f"{self.name}"


    def __repr__(self):
        return self.__str__()





def getGlyphs(inputPath, delim, extension, no_lig, no_vs16):
    """
    - Validates glyph image paths from the input path.
    - Returns a list of glyph objects, including important special control glyphs.
    """

    dir = pathlib.Path(inputPath).absolute()
    inputGlyphs = list(dir.glob("*." + extension))
    glyphs = []

    vs16Allowed = not no_vs16


    glyphs.append(glyph([0x0], '.notdef', None))
    glyphs.append(glyph([0xd], 'CR', None))
    glyphs.append(glyph([0x20], 'space', None))



    # process all of the input glyphs
    # --------------------------------------------------------------------

    vs16Presence = False
    zwjPresence = False

    for g in inputGlyphs:
        codepoints = []

        # try to check if every part of the
        # filename stem is a valid hexadecimal number.

        try:
            codepoints = [int(hex, 16) for hex in g.stem.split(delim)]

        except ValueError as e:
            log.out(f'!!! One of your glyph files is not named as hexadecimal numbers.', 31)
            log.out(f'!!! It is \'{g}\'', 31)


        # tidy instances of fe0f before adding them to the glyph list

        if int('fe0f', 16) in codepoints:

            vs16Presence = vs16Allowed
            codepoints.remove(int('fe0f', 16))

            if len(codepoints) == 1:
                glyphs.append(glyph(codepoints, None, g, vs16Allowed))

            else:
                glyphs.append(glyph(codepoints, None, g, False))

        else:
            glyphs.append(glyph(codepoints, None, g, False))

        if int('200d', 16) in codepoints:
            zwjPresence = True


    # Add vs16 to the glyphs if one of the
    # processed codepoint chains contains U+fe0f.

    if vs16Presence:
        glyphs.append(glyph([0xfe0f], 'VS16', None))

    # Add ZWJ to the glyphs if one of the
    # processed codepoint chains contains U+200d.

    if zwjPresence:

        # The glyph.name is 'u200d' because that's how other
        # parts of the app will interpret 200d as a GlyphID.
        # DO NOT CHANGE IT.

        glyphs.append(glyph([0x200d], 'u200d', None))





    # test for duplicates
    # --------------------------------------------------------------------

    for id1, g1 in enumerate(glyphs):
        for id2, g2 in enumerate(glyphs):
            if g1.name == g2.name:
                if id1 != id2:
                    raise Exception(f"One of your glyphs ({g1.imagePath}), when stripped of VS16 (fe0f), matches another ({g2.imagePath}). There can't be duplicates in this scenario.")





    # validate ligatures
    # --------------------------------------------------------------------

    singleGlyphCodepoints = []
    ligatures = []

    #TEMP
    singleGlyphs = []

    for g in glyphs:
        if len(g.codepoints) > 1:
            ligatures.append(g)
        else:
            singleGlyphCodepoints.append(g.codepoints[0])
            singleGlyphs.append(g)


    for g in ligatures:
        for codepoint in g.codepoints:
            if codepoint not in singleGlyphCodepoints:
                raise Exception(f"One of your ligatures ({g.imagePath}) does not have all non-service codepoints represented as glyphs ({glyphName(codepoint)}). All components of all ligatures must be represented as glyphs (apart from fe0f and 200d).")


    if no_lig:
        return singleGlyphs
    else:
        return glyphs

import pathlib

import log




class glyph:

    def __init__(self, codepoints, name, imagePath=None):

        if codepoints:
            self.codepoints = codepoints
        elif imagePath:
            self.codepoints = [int(hex, 16) for hex in imagePath.stem.split(delim)]
        else:
            raise ValueError(f"Tried to make glyph object '{name}' but doesn't have a codepoint AND it doesn't have an image path.")

        if name:
            self.name = name
        else:
            self.name = "u" + imagePath.stem

        self.imagePath = imagePath




    def __str__(self):
        return f"glyph<{self.codepoints}, {self.name}, {self.imagePath}>"


    def __repr__(self):
        return self.__str__()





def getGlyphs(inputPath, delim, extension):
    """
    - Validates glyph image paths from the input path.
    - Returns a list of glyph objects, including important special control glyphs.
    """

    dir = pathlib.Path(inputPath).absolute()
    inputGlyphs = list(dir.glob("*." + extension))
    glyphs = []


    glyphs.append(glyph([0x0], '.notdef', None))
    glyphs.append(glyph([0xd], 'CR', None))
    glyphs.append(glyph([0x20], 'space', None))


    # try to check if every part of the
    # filename stem is a valid hexadecimal number.

    for g in inputGlyphs:
        try:
            codepoints = [int(hex, 16) for hex in g.stem.split(delim)]
            glyphs.append(glyph(codepoints, None, g))

        except ValueError as e:
            log.out(f'!!! One of your glyph files is not named as a hexadecimal number.', 31)
            log.out(f'!!! It is \'{glyph.name}\'', 31)


    return glyphs

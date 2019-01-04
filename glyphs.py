import pathlib

import log



def getGlyphs(inputPath, delim, extension):
    """
    Gets glyph images from the input path.
    It also validates the glyphs before returning them,
    raising errors when there aren't any or the result isn't expected.
    """

    dir = pathlib.Path(inputPath)
    glyphs = list(dir.glob("*." + extension))


    # try to check if every part of the
    # filename stem is a valid hexadecimal number.

    for glyph in glyphs:
        try:
            testints = [int(hex, 16) for hex in glyph.stem.split(delim)]
        except ValueError as e:
            log.out(f'!!! One of your glyph files is not named as a hexadecimal number.', 31)
            log.out(f'!!! It is \'{glyph.name}\'', 31)

    return glyphs

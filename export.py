import subprocess
import pathlib

import log
from assembler import assembler
from glyphs import getGlyphs



def compileTTX(ttxFile, outputPath):
    """
    Invokes ttx

    Making this it's own function now so I can selectively invoke it.
    """

    # feed the assembled TTX as input to the ttx commaand line tool.
    cmd_ttx = ['ttx', '-o', outputPath, ttxFile]

    # try to export temporary PNG
    try:
        r = subprocess.run(cmd_ttx, stdout=subprocess.DEVNULL).returncode
    except Exception as e:
        raise Exception('TTX compiler invocation failed: ' + str(e))
    if r:
        raise Exception('TTX compiler returned error code: ' + str(r))




def createFont(fontFormat, outputPath, manifest, images):
    """
    Calls the functions that assemble and create a font.
    """

    log.out(f'Assembling {fontFormat} font...')
    ttxString = assembler(fontFormat, manifest, images)


    opp = pathlib.Path(outputPath).absolute()

    ttxDestination = opp / (fontFormat + '.ttx')

    try:
        with open(ttxDestination, 'w') as file:
            file.write(ttxString)
    except Exception:
        raise Exception('Could not write to file')

    compileTTX(ttxDestination, outputPath)






def export(manifest, inputPath, outputPath, outputFormats, delim):
    """
    Performs a variety of processing and validation tasks
    related to font format, then initiates font creation once those
    have passed.
    """

    # determine what image formats need to be used
    # (also check if the output formats are valid)
    # ------------------------------------------------

    glyphImageFormats = set()

    log.out(f'Checking output format(s)...', 36)
    for f in outputFormats:
        if f == 'svginot':
            glyphImageFormats.add('svg')
        elif f in ['sbix', 'sbixios', 'cbdtcblc']:
            glyphImageFormats.add('png')
        else:
            raise ValueError(f"Invalid output format: {f}")

    log.out(f'Output format(s) verified.', 32)


    # check the image sets for each format.
    # ------------------------------------------------

    glyphImages = dict()

    log.out(f'Checking glyph images...', 36)
    for format in glyphImageFormats:

        formatInput = pathlib.Path(inputPath) / manifest['glyphs'][format]
        glyphList = getGlyphs(formatInput, delim, format)

        if not glyphList:
            log.out(f'!!! There are no {format} glyph images!!', 31)
        else:
            log.out(f'{format} files verified.', 32)
            glyphImages[format] = glyphList



    # assemble each font format.
    # ------------------------------------------------

    for f in outputFormats:

        if f == 'svginot':
            createFont(f, outputPath, manifest, glyphImages['svg'])

        elif f in ['sbix', 'sbixios', 'cbdtcblc']:
            createFont(f, outputPath, manifest, glyphImages['png'])

import subprocess
from xml.dom import minidom

import log
from assembler import assembler
from glyphs import getGlyphs



def ttx(ttxString, inputPath, outputPath):
    """
    Invokes ttx

    Making this it's own function now so I can selectively invoke it.
    """
    # write ttx to temporary file
    with open("temp.ttx", 'w') as f:
        f.write(ttxString)

    # feed the assembled TTX as input to the ttx commaand line tool.
    cmd_ttx = ['ttx', 'temp.ttx', '-o', outputPath]

    # try to export temporary PNG
    try:
        r = subprocess.run(cmd_ttx, stdout=subprocess.DEVNULL).returncode
    except Exception as e:
        raise Exception('TTX compiler invocation failed: ' + str(e))
    if r:
        raise Exception('TTX compiler returned error code: ' + str(r))


def export(manifest, inputPath, outputPath, outputFormats, delim):

    glyphImageFormats = set()
    for f in outputFormats:
        if f == 'svginot':
            glyphImageFormats.add('svg')
        elif f in ['sbix', 'sbixios', 'cbdtcblc']:
            glyphImageFormats.add('png')
        else:
            raise ValueError(f"Invalid output format: {f}")


    print(glyphImageFormats)

    glyphImages = dict()

    log.out(f'Checking glyph images...', 36)

    for format in glyphImageFormats:
        glyphList = getGlyphs(inputPath, delim, format)

        if not glyphList:
            log.out(f'!!! There are no {format} glyph images!!', 31)
        else:
            log.out(f'{format} files verified.', 32)
            glyphImages[format] = glyphList


    ttxString = assembler(manifest)

    # prettyyyy~~~~
    reparsedXML = minidom.parseString(ttxString)
    prettyOutput = reparsedXML.toprettyxml(indent="  ")
    #print(prettyOutput)

    #ttx(ttxString, inputPath, outputPath)

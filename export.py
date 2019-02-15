import subprocess
import pathlib

import log
from assembler import assembler
from glyphs import getGlyphs
from ios import compileiOSConfig
from format import formats

def compileTTX(input, output):
    """
    Invokes ttx

    Making this it's own function now so I can selectively invoke it.
    """

    # feed the assembled TTX as input to the ttx commaand line tool.
    cmd_ttx = ['ttx', '-q', '-o', output, input]

    # try to export temporary PNG
    try:
        r = subprocess.run(cmd_ttx, stdout=subprocess.DEVNULL).returncode
    except Exception as e:
        raise Exception('TTX compiler invocation failed: ' + str(e))
    if r:
        raise Exception('TTX compiler returned error code: ' + str(r))


def writeFile(path, contents, exceptionString):
    try:
        with open(path, 'wb') as file:
            file.write(contents)
    except Exception:
        raise Exception(exceptionString)



def createFont(fontFormat, outputPath, manifest, allGlyphs, ttx_output, dev_ttx_output):
    """
    Calls the functions that assemble and create a font.
    """

    log.out(f'[{fontFormat}]', 35)


    # VARIABLES
    extension = formats[fontFormat]["extension"]
    imageFormat = formats[fontFormat]["imageFormat"]
    glyphs = allGlyphs[imageFormat]

    outputAbsolute = pathlib.Path(outputPath).absolute()





    # assemble TTX
    log.out(f'Assembling initial TTX...')
    originalTTX = assembler(fontFormat, manifest, glyphs)
    log.out(f'Initial TTX successfully assembled.', 32)


    # save TTX
    log.out(f'Saving initial TTX to file...')
    originalTTXPath = outputAbsolute / (f"{fontFormat}_initial.ttx")
    writeFile(originalTTXPath, originalTTX, 'Could not write initial TTX to file')
    log.out(f'Initial TTX saved.', 32)


    # compile TTX to font
    log.out(f'Compiling font...')
    outputFontPath = outputAbsolute / (fontFormat + extension)
    compileTTX(originalTTXPath, outputFontPath)
    log.out(f'Font compiled.', 32)


    # --dev-ttx flag
    if not dev_ttx_output:
        log.out(f'Deleting initial TTX...')
        originalTTXPath.unlink() #delete


    # -ttx flag
    if ttx_output:
        log.out(f'Compiling finished TTX..')
        afterExportTTX = outputAbsolute / (f"{fontFormat}_finished.ttx")
        compileTTX(outputFontPath, afterExportTTX)


    # iOS Configuration Profile compilation
    # (must come after everything else)
    if formats[fontFormat]["iOSCompile"]:
        log.out(f'Compiling iOS Configuration Profile...')
        configString = compileiOSConfig(manifest, outputFontPath, outputPath)
        configPath = outputAbsolute / (f"{fontFormat}.mobileconfig")
        writeFile(configPath, configString, 'Could not write iOS Configuration Profile to file')

        log.out(f'Deleting the original Font...')
        outputFontPath.unlink() #delete

    log.out(f'Done!!!', 32)






def export(manifest, inputPath, outputPath, outputFormats, delim, ttx_output, dev_ttx_output, no_lig, no_vs16):
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

        # check if it's in the list of accepted formats
        if f not in formats:
            raise ValueError(f"Invalid output format: {f}")

        # check what formats are needed
        if formats[f]["imageFormat"] == 'svg':
            glyphImageFormats.add('svg')
        elif formats[f]["imageFormat"] == 'png':
            glyphImageFormats.add('png')


    log.out(f'Output format(s) verified.', 32)




    # check the image sets for each format.
    # ------------------------------------------------

    allGlyphs = dict()

    log.out(f'Checking glyph images...', 36)
    for format in glyphImageFormats:

        formatInput = pathlib.Path(inputPath) / manifest['glyphs'][format]
        glyphList = getGlyphs(formatInput, delim, format, no_lig, no_vs16)

        if not glyphList:
            log.out(f'!!! There are no {format} glyph images!!', 31)
        else:
            log.out(f'{format} files verified.', 32)
            allGlyphs[format] = glyphList




    # assemble each font format.
    # ------------------------------------------------

    for f in outputFormats:
        createFont(f, outputPath, manifest, allGlyphs, ttx_output, dev_ttx_output)

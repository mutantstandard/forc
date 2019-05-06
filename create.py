import subprocess
import pathlib

import log
from assembler import assembler
from ios import compileiOSConfig
from format import formats



# create.py
# -------------------------------
#
# The routines and outline processes responsible for one single font compilation cycle.




def compileTTX(input, output):
    """
    Invokes the TTX compiler and attempts to compile a font with it.
    """

    # feed the assembled TTX as input to the ttx command line tool.
    cmd_ttx = ['ttx', '-q', '-o', output, input]

    # try to export temporary PNG
    try:
        r = subprocess.run(cmd_ttx, stdout=subprocess.DEVNULL).returncode
    except Exception as e:
        raise Exception('TTX compiler invocation failed: ' + str(e))
    if r:
        raise Exception('TTX compiler returned error code: ' + str(r))


def writeFile(path, contents, exceptionString):
    """
    A basic repetitive function that tries to write something to a file.
    """
    try:
        with open(path, 'wb') as file:
            file.write(contents)
    except Exception:
        raise Exception(exceptionString)





def createFont(fontFormat, outputPath, manifest, glyphs, ttx_output, dev_ttx_output, afsc, no_vs16):
    """
    Calls the functions that assemble and create a font.
    """

    log.out(f'[{fontFormat}]', 36)


    # VARIABLES
    extension = formats[fontFormat]["extension"]
    imageFormat = formats[fontFormat]["imageFormat"]

    outputAbsolute = pathlib.Path(outputPath).absolute()





    # assemble TTX
    log.out(f'Assembling initial TTX...')
    originalTTX = assembler(fontFormat, manifest, glyphs, afsc, no_vs16)
    log.out(f'Initial TTX successfully assembled.', 32)


    # save TTX
    log.out(f"Saving forc's assembled (initial) TTX to file...")
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
        log.out(f'Deleting the initial TTX...')
        originalTTXPath.unlink() #delete


    # -ttx flag
    if ttx_output:
        log.out(f'Compiling a finished TTX from the font file..')
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

    log.out(f'This format has been successfully exported.', 32)

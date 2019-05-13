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

    log.out(f'{fontFormat}', 96)
    log.out("-----------------", 90)


    # VARIABLES
    # ------------------------------------------------------
    extension = formats[fontFormat]["extension"]
    imageFormat = formats[fontFormat]["imageFormat"]

    # output folder
    outputAbsolute = pathlib.Path(outputPath).absolute()


    # filenames
    # the user setting custom filenames in the manifest is optional.
    # If none are given, just use the font format as the base filename.

    if "filenames" in manifest["metadata"]:
        filename = manifest['metadata']['filenames'][fontFormat]
    else:
        filename = fontFormat

    originalTTXPath = outputAbsolute / (filename + "_dev.ttx")
    outputFontPath = outputAbsolute / (filename + extension)
    afterExportTTX = outputAbsolute / (filename + ".ttx")





    # DOING THE THING
    # ------------------------------------------------------

    # assemble TTX
    log.out(f'Assembling initial TTX...')
    originalTTX = assembler(fontFormat, manifest, glyphs, afsc, no_vs16)
    log.out(f'Initial TTX successfully assembled.\n', 32)


    # save TTX
    log.out(f"📝 Saving forc's assembled (initial) TTX to file...")
    writeFile(originalTTXPath, originalTTX, 'Could not write initial TTX to file')
    log.out(f'✅ Initial TTX saved.\n', 32)


    # compile TTX to font
    log.out(f'⚙️  Compiling font...')
    compileTTX(originalTTXPath, outputFontPath)
    log.out(f'✅ Font compiled.\n', 32)


    # compile back to TTX
    #
    # This is because TTX doesn't catch all font errors on the first pass.
    log.out(f'⚙️  Testing font by compiling it back to TTX...')
    compileTTX(outputFontPath, afterExportTTX)
    log.out(f'✅ Font testing OK.\n', 32)

    # --dev-ttx flag
    if not dev_ttx_output:
        log.out(f'🗑  Deleting the initial TTX...')
        originalTTXPath.unlink() #delete

    # -ttx flag
    if not ttx_output:
        log.out(f'🗑  Deleting second-pass TTX...')
        afterExportTTX.unlink() #delete


    # iOS Configuration Profile compilation
    # (must come after everything else)
    if formats[fontFormat]["iOSCompile"]:
        log.out(f'Compiling iOS Configuration Profile...')
        configString = compileiOSConfig(manifest, outputFontPath, outputPath)
        configPath = outputAbsolute / (f"{fontFormat}.mobileconfig")
        writeFile(configPath, configString, 'Could not write iOS Configuration Profile to file')

        log.out(f'🗑  Deleting the original Font...')
        outputFontPath.unlink() #delete

    log.out(f'✅ This font has been successfully created.\n\n', 32)

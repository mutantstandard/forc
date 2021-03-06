import pathlib
import log
import shutil

import files
from format import formats


def createFont(formatData, outPath, tempPath, filename, flags, font):
    """
    Calls the functions that assemble and create a font via forc's TTX compiler method.
    """



    # VARIABLES
    # ------------------------------------------------------
    extension = formatData["extension"]
    imageFormat = formatData["imageFormat"]
    formatName = formatData["name"]


    originalTTXPath = tempPath / (filename + "_dev.ttx")
    afterExportTTX = tempPath / (filename + ".ttx")

    outFontPath = tempPath / (filename + extension)


    # COMPILER
    # ------------------------------------------------------
    log.out(f"[ttx compiler]", 90)

    # save TTX
    log.out(f"- Saving forc's assembled (initial) TTX to file...", 90)

    files.writeFile(originalTTXPath, font.toTTX(asString=True), 'Could not write initial TTX to file')

    # --dev-ttx flag
    if flags["dev_ttx_output"]:
        shutil.copy(str(originalTTXPath), str(outPath / (filename + "_dev.ttx")))


    log.out(f'- Compiling font...', 90)
    files.compileTTX(originalTTXPath, outFontPath)




    # TESTING
    # ------------------------------------------------------
    # We use TTX again because TTX actually doesn't catch all font errors on the first pass.

    if not flags['no_test'] and flags["ttx_output"]:
        log.out(f'- Testing font by compiling it back to TTX...', 90)
        files.compileTTX(outFontPath, afterExportTTX)

        # -ttx flag
        shutil.copy(str(afterExportTTX), str(outPath / (filename + ".ttx")))


    elif not flags['no_test']:
        log.out(f'- Testing font by compiling it back to TTX...', 90)
        files.compileTTX(outFontPath, afterExportTTX)


    return outFontPath

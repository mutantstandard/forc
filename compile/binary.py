import pathlib
import log
import shutil

import files
from format import formats






def createFont(formatData, outPath, tempPath, filename, flags, font):
    """
    Calls the functions that assemble and create a font via forc's internal compiler method.
    """



    # VARIABLES
    # ------------------------------------------------------
    extension = formatData["extension"]
    imageFormat = formatData["imageFormat"]
    formatName = formatData["name"]

    outFontPath = tempPath / (filename + extension)
    testTTX = tempPath / (filename_test + ".ttx")


    # ASSEMBLER -> TTX
    # ------------------------------------------------------
    log.out(f"[forc compiler]", 90)

    # save TTX
    log.out(f"- Saving forc's assembled (initial) TTX to file...", 90)

    files.writeFile(outFontPath, font.toBytes(), 'Could not write binary font to file')

    log.out(f'- Testing font by running it through TTX..', 90)
    files.compileTTX(outFontPath, testTTX)

    return outFontPath

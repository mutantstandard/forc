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
    testTTX = tempPath / (filename + "_test.ttx")


    # ASSEMBLER -> TTX
    # ------------------------------------------------------
    log.out(f"[forc compiler]", 90)

    # save TTX
    log.out(f"- Packing font data into binary and writing it to file...", 90)

    files.writeFile(outFontPath, font.toBytes(), 'Could not write binary font to file')

    log.out(f'- Testing font by attempting to decompile as TTX..', 90)
    files.compileTTX(outFontPath, testTTX)

    return outFontPath

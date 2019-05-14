import subprocess
import pathlib
import log
import pathlib
import shutil

import files
from format import formats
from compile.ttx.assembler import assembler

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







def createFont(formatData, outPath, tempPath, filename, manifest, glyphs, ttx_output, dev_ttx_output, afsc, no_vs16):
    """
    Calls the functions that assemble and create a font via TTX.
    """



    # VARIABLES
    # ------------------------------------------------------
    extension = formatData["extension"]
    imageFormat = formatData["imageFormat"]
    formatName = formatData["name"]


    originalTTXPath = tempPath / (filename + "_dev.ttx")
    afterExportTTX = tempPath / (filename + ".ttx")

    outFontPath = tempPath / (filename + extension)






    # DOING THE THING
    # ------------------------------------------------------

    # assemble TTX
    log.out(f'🛠  Assembling initial TTX...')
    originalTTX = assembler(formatName, manifest, glyphs, afsc, no_vs16)
    log.out(f'✅ Initial TTX successfully assembled.\n', 32)


    # save TTX
    log.out(f"⚙️  Compiling and testing font...")
    log.out(f"- Saving forc's assembled (initial) TTX to file...", 90)

    files.writeFile(originalTTXPath, originalTTX, 'Could not write initial TTX to file')


    # compile TTX to font
    log.out(f'- Compiling font...', 90)
    compileTTX(originalTTXPath, outFontPath)


    # compile back to TTX
    #
    # This is because TTX doesn't catch all font errors on the first pass.
    log.out(f'- Testing font by compiling it back to TTX...', 90)
    compileTTX(outFontPath, afterExportTTX)


    log.out(f'✅ Compiling and testing OK.\n', 32)



    # --dev-ttx flag
    if dev_ttx_output:
        shutil.copy(str(originalTTXPath), str(outPath / (filename + "_dev.ttx")))

    # -ttx flag
    if ttx_output:
        shutil.copy(str(originalTTXPath), str(outPath / (filename + ".ttx")))


    return outFontPath

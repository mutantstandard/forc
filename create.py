import subprocess
import pathlib
import log
import shutil

import files
import compile.ttx.create
import compile.ios.create
from format import formats


def createFont(fontFormat, outputPath, manifest, glyphs, compiler, ttx_output, dev_ttx_output, afsc, no_vs16):

    log.out(f'{fontFormat}', 96)
    log.out("-----------------", 90)

    # output folder
    outPath = pathlib.Path(outputPath).absolute()
    tempPath = outPath / '.forc_tmp'

    files.tryDirectory(tempPath, "dir", "temporary font build folder", tryMakeFolder=True)


    # filenames
    # the user setting custom filenames in the manifest is optional.
    # If none are given, just use the font format as the base filename.

    if "filenames" in manifest["metadata"]:
        filename = manifest['metadata']['filenames'][fontFormat]
    else:
        filename = fontFormat

    # format information
    formatData = formats[fontFormat]




    if compiler is 'ttx':
        tempFontPath = compile.ttx.create.createFont(formatData, outPath, tempPath, filename, manifest, glyphs, ttx_output, dev_ttx_output, afsc, no_vs16)

    if formats[fontFormat]["iOSCompile"]:
        compile.ios.create.createPackage(formatData, filename, outPath, tempFontPath, manifest)
    else:
        shutil.copy(str(tempFontPath), str(outPath / (filename + formatData["extension"])))




    # delete the temporary folder (recursively)
    log.out(f'🗑  Cleaning up...')
    shutil.rmtree(tempPath)

    log.out(f'✅ Format finished!\n\n', 32)

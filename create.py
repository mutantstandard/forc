import subprocess
import pathlib
import log

import compile.ttx.create
import compile.ios.create
from format import formats


def createFont(fontFormat, outputPath, manifest, glyphs, ttx_output, dev_ttx_output, afsc, no_vs16):

    log.out(f'{fontFormat}', 96)
    log.out("-----------------", 90)

    # output folder
    outPathAbsolute = pathlib.Path(outputPath).absolute()
    tempPath = outPathAbsolute / '.tmp'


    # filenames
    # the user setting custom filenames in the manifest is optional.
    # If none are given, just use the font format as the base filename.

    if "filenames" in manifest["metadata"]:
        filename = manifest['metadata']['filenames'][fontFormat]
    else:
        filename = fontFormat

    # format information
    formatData = formats[fontFormat]


    outputFontPath = compile.ttx.create.createFont(formatData, outPathAbsolute, tempPath, filename, manifest, glyphs, ttx_output, dev_ttx_output, afsc, no_vs16)

    if formats[fontFormat]["iOSCompile"]:
        compile.ios.create.createPackage(formatData, filename, outPathAbsolute, outputFontPath, manifest)

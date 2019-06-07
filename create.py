import subprocess
import pathlib
import log
import shutil

import files
from font import TTFont
import compile.ttx
import compile.ios.create
from format import formats


def createFont(fontFormat, outputPath, manifest, glyphs, compiler, flags):

    log.out(f'{fontFormat}', 96)
    log.out("-----------------", 90)


    # prepare some variables
    # --------------------------------------------------------------

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




    # create the font!
    # --------------------------------------------------------------
    log.out(f'🛠  Assembling font...')
    emojiFont = TTFont(formatData["name"], manifest, glyphs, flags)
    log.out(f'✅ Font successfully assembled.\n', 32)


    # pass it to compilers and packagers
    # --------------------------------------------------------------
    log.out(f"⚙️  Compiling and testing font...")


    if compiler == 'ttx':
        tempFontPath = compile.ttx.createFont(formatData, outPath, tempPath, filename, flags, emojiFont)
    elif compiler == 'forc':
        tempFontPath = compile.binary.createFont(formatData, outPath, tempPath, filename, flags, emojiFont)
    else:
        raise ValueError("Something went wrong with the build process. I'm not able to run the font data through a compiler.")

    log.out(f'✅ Compiling and testing OK.\n', 32)


    if formats[fontFormat]["iOSCompile"]:
        log.out(f"⚙️  Packaging font...")
        compile.ios.create.createPackage(formatData, filename, outPath, tempFontPath, manifest)
        log.out(f'✅ Packaging OK.\n', 32)

    else:
        shutil.copy(str(tempFontPath), str(outPath / (filename + formatData["extension"])))


    # finish!
    # --------------------------------------------------------------

    # delete the temporary folder (recursively)
    log.out(f'🗑  Cleaning up...')
    shutil.rmtree(tempPath)

    log.out(f'✅ Format finished!\n\n', 32)

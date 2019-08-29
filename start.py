import pathlib

import log
import files
from create import createFont
from manifest.manifest import checkTransformManifest
from validate.aliases import validateAliases
from glyphProc import getGlyphs
from format import formats, compilers



# start.py
# -------------------------------
#
# All of the data gathering and validation required before initiating font export.
# Also initiates font export when all of these things are completed and satisfactory.


def start( inputPath
          , outputPath
          , manifestPath
          , aliasesPath
          , delim_codepoint

          , outputFormats
          , compiler
          , flags
          ):
    """
    Performs a variety of initial data gathering and validation tasks,
    designed to make sure all of the user-given data is valid and usable.

    Once this has all been validated, it starts the font making process.
    """

    log.out(f'\nFetching resources...', 35)
    log.out("----------------------------------", 90)


    # check folder stuff
    # ------------------------------------------------

    log.out(f'Checking file + folder locations...')

    inputPathPath = pathlib.Path(inputPath).absolute()
    files.tryUserDirectory(inputPathPath, "dir", "input folder")

    outputPathPath = pathlib.Path(outputPath).absolute()
    files.tryUserDirectory(outputPathPath, "dir", "output folder", tryMakeFolder=True)

    manifestPathPath = pathlib.Path(manifestPath).absolute()
    files.tryUserDirectory(manifestPathPath, "file", "manifest file")

    if aliasesPath:
        aliasesPathPath = pathlib.Path(aliasesPath).absolute()
        files.tryUserDirectory(aliasesPathPath, "file", "aliases file")

    log.out(f'File + folder locations OK!\n', 32)




    # determine what image formats need to be used
    # (also check if the output formats are valid)
    # ------------------------------------------------

    glyphImageFormats = set()

    log.out(f'Checking output parameters...')
    for f in outputFormats:

        # check if it's in the list of accepted formats
        if f not in formats:
            raise ValueError(f"'{f}' isn't a valid output format!")

        # check what formats are needed
        if formats[f]["imageFormat"] == 'svg':
            glyphImageFormats.add('svg')
        elif formats[f]["imageFormat"] == 'png':
            glyphImageFormats.add('png')

    log.out(f'Output format(s) OK!\n', 32)




    # check compiler
    # ------------------------------------------------
    if compiler not in compilers:
        raise ValueError(f"You gave '{compiler}' as the compiler to use. This doesn't exist in forc. Check the help menu (-h) to see which compilers you can use.")



    # manifest
    # ------------------------------------------------

    log.out(f'Getting + checking manifest data...')
    manifest = files.loadJson(manifestPath, "manifest file")
    checkTransformManifest(outputFormats, manifest)

    log.out(f'Manifest OK!.\n', 32)



    # aliases (file)
    # ------------------------------------------------

    if aliasesPath:
        log.out(f'Getting + checking aliases data...')
        aliases = files.loadJson(aliasesPath, "aliases file")
        validateAliases(aliases)
        log.out(f'Aliases OK!.\n', 32)
    else:
        aliases = None



    # glyphs
    # ------------------------------------------------

    log.out(f'Getting + checking glyphs...')
    glyphs = getGlyphs(inputPathPath, manifest, aliases, delim_codepoint, glyphImageFormats, flags)
    log.out(f'Glyphs OK!\n', 32)


    log.out(f'All resources OK!', 32)


    # assemble each font format.
    # ------------------------------------------------

    log.out(f'Starting font compilation...\n\n', 35)

    for f in outputFormats:
        createFont(f, outputPath, manifest, glyphs, compiler, flags)

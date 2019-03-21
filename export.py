import pathlib
import json

import log
from create import createFont
from validate.manifest import validateManifest
from validate.aliases import validateAliases
from glyphs import getGlyphs
from format import formats




def tryDirectory(absolutePath, dirOrFile, dirName, tryMakeFolder=False):
    if not absolutePath.exists():
        if not tryMakeFolder:
            raise ValueError(f"The {dirName} you gave ({absolutePath}) doesn't exist.")
        else:
            try:
                absolutePath.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise Exception(f"Couldn't make the {dirName} ({absolutePath}). ({e})" )
    else:
        if dirOrFile == "file" and absolutePath.is_dir():
                raise ValueError(f"The {dirName} you gave ({absolutePath}) is a folder, not a file.")
        elif dirOrFile == "dir" and absolutePath.is_file():
                raise ValueError(f"The {dirName} you gave ({absolutePath}) is a file, not a folder.")




def loadJson(jsonPath, fileName):
    try:
        with open(jsonPath, "r") as read_file:
            return json.load(read_file)
    except Exception as e:
        raise ValueError(f"Loading the {fileName} file failed! ({e})")









def export( inputPath
          , outputPath
          , manifestPath
          , aliasesPath

          , outputFormats
          , delim_codepoint

          , ttx_output
          , dev_ttx_output

          , no_vs16
          , nusc
          , afsc

          , no_lig
          ):
    """
    Performs a variety of processing and validation tasks
    related to font format, then initiates font creation once those
    have passed.
    """

    log.out(f'Fetching resources...', 35)



    # check folder stuff
    # ------------------------------------------------

    log.out(f'Checking file + folder locations...')

    inputPathPath = pathlib.Path(inputPath).absolute()
    tryDirectory(inputPathPath, "dir", "input folder")

    outputPathPath = pathlib.Path(outputPath).absolute()
    tryDirectory(outputPathPath, "dir", "output folder", tryMakeFolder=True)

    manifestPathPath = pathlib.Path(manifestPath).absolute()
    tryDirectory(manifestPathPath, "file", "manifest file")

    if aliasesPath:
        aliasesPathPath = pathlib.Path(aliasesPath).absolute()
        tryDirectory(aliasesPathPath, "file", "aliases file")

    log.out(f'File + folder locations OK!', 32)




    # determine what image formats need to be used
    # (also check if the output formats are valid)
    # ------------------------------------------------

    glyphImageFormats = set()

    log.out(f'Checking output format(s)...')
    for f in outputFormats:

        # check if it's in the list of accepted formats
        if f not in formats:
            raise ValueError(f"'{f}' isn't a valid output format!")

        # check what formats are needed
        if formats[f]["imageFormat"] == 'svg':
            glyphImageFormats.add('svg')
        elif formats[f]["imageFormat"] == 'png':
            glyphImageFormats.add('png')

    log.out(f'Output format(s) OK!', 32)



    # manifest
    # ------------------------------------------------

    log.out(f'Getting + Checking manifest JSON...')
    manifest = loadJson(manifestPath, "manifest file")
    validateManifest(outputFormats, manifest)

    log.out(f'Manifest OK!.', 32)



    # aliases (file)
    # ------------------------------------------------

    if aliasesPath:
        log.out(f'Getting + Checking aliases JSON...')
        aliases = loadJson(aliasesPath, "aliases file")
        validateAliases(aliases)
        log.out(f'Aliases OK!.', 32)
    else:
        aliases = None



    # glyphs
    # ------------------------------------------------

    log.out(f'Getting + checking glyphs...')
    glyphs = getGlyphs(inputPathPath, aliases, delim_codepoint, glyphImageFormats, no_lig, no_vs16, nusc)
    log.out(f'Glyphs OK!', 32)



    log.out(f'All resources OK!', 32)


    # assemble each font format.
    # ------------------------------------------------

    log.out(f'Starting font compilation...', 35)

    for f in outputFormats:
        createFont(f, outputPath, manifest, glyphs, ttx_output, dev_ttx_output, afsc, no_vs16)

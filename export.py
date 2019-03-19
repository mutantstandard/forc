import pathlib
import json

import log
from create import createFont
from validate.manifest import validateManifest
from validate.aliases import validateAliases
from glyphs import getGlyphs
from format import formats




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

          , no_lig
          ):
    """
    Performs a variety of processing and validation tasks
    related to font format, then initiates font creation once those
    have passed.
    """

    log.out(f'Fetching resources...', 35)

    # check if the input and output folders are valid.
    inputPathPath = pathlib.Path(inputPath).absolute()
    outputPathPath = pathlib.Path(outputPath).absolute()
    manifestPathPath = pathlib.Path(manifestPath).absolute()






    # deal with input/output/manifest directories
    # ------------------------------------------------

    # check if the input directory exists.

    log.out(f'Checking input/output directories...')
    if not inputPathPath.exists():
        raise ValueError(f"Your input folder - {inputPathPath} - is not a real directory.")
    elif inputPathPath.is_file():
        raise ValueError(f"Your input folder - {inputPathPath} - is a file, not a directory.")



    # try to make the output directory.

    if not outputPathPath.exists():
        try:
            outputPathPath.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise Exception("Couldn't make the output folder '{outputPathPath}':" + str(e))


    if not manifestPathPath.exists():
        raise ValueError(f"Your the place where you said the manifest would be ({manifestPathPath}) doesn't exist.")
    elif manifestPathPath.is_dir():
        raise ValueError(f"Your the place where you said the manifest would be ({manifestPathPath}) is a directory, not a file.")


    if aliasesPath:
        aliasesPathPath = pathlib.Path(aliasesPath).absolute()

        if not aliasesPathPath.exists():
            raise ValueError(f"Your the place where you said the aliases would be ({aliasesPathPath}) doesn't exist.")
        if aliasesPathPath.is_dir():
            raise ValueError(f"Your the place where you said the aliases would be ({aliasesPathPath}) is a directory, not a file.")


    log.out(f'Input/output directories OK!', 32)




    # determine what image formats need to be used
    # (also check if the output formats are valid)
    # ------------------------------------------------

    glyphImageFormats = set()

    log.out(f'Checking output format(s)...')
    for f in outputFormats:

        # check if it's in the list of accepted formats
        if f not in formats:
            raise ValueError(f"'{f}' isn't an output format!")

        # check what formats are needed
        if formats[f]["imageFormat"] == 'svg':
            glyphImageFormats.add('svg')
        elif formats[f]["imageFormat"] == 'png':
            glyphImageFormats.add('png')

    log.out(f'Output format(s) OK!', 32)





    # try to load and check the manifest.
    # ------------------------------------------------


    log.out(f'Getting + Checking manifest JSON...')
    try:
        with open(manifestPath, "r") as read_file:
            manifest = json.load(read_file)
    except Exception as e:
        raise Exception('Loading the manifest file failed!' + str(e))

    validateManifest(outputFormats, manifest)

    log.out(f'Manifest OK!.', 32)



    # try to load and check the aliases if the user provided any.
    # ------------------------------------------------

    if aliasesPath:
        log.out(f'Getting + Checking aliases JSON...')
        try:
            with open(aliasesPath, "r") as read_file:
                aliases = json.load(read_file)
        except Exception as e:
            raise Exception('Loading the aliases file failed! ' + str(e))

        validateAliases(aliases)

        log.out(f'Aliases OK!.', 32)
    else:
        aliases = None






    # check the image sets for each format.
    # ------------------------------------------------


    log.out(f'Getting + checking glyphs...')
    glyphs = getGlyphs(inputPathPath, aliases, delim_codepoint, glyphImageFormats, no_lig, no_vs16, nusc)

    log.out(f'Glyphs OK!', 32)



    log.out(f'All resources OK!', 32)


    # assemble each font format.
    # ------------------------------------------------

    log.out(f'Starting font compilation...', 35)

    for f in outputFormats:
        createFont(f, outputPath, manifest, glyphs, ttx_output, dev_ttx_output)

import pathlib
import json

import log
from create import createFont
from glyphs import getGlyphs
from format import formats




def export(manifestPath, inputPath, outputPath, outputFormats, delim, ttx_output, dev_ttx_output, no_lig, no_vs16, nsc):
    """
    Performs a variety of processing and validation tasks
    related to font format, then initiates font creation once those
    have passed.
    """

    log.out(f'Export started!', 35)

    # check if the input and output folders are valid.
    inputPathPath = pathlib.Path(inputPath).absolute()
    outputPathPath = pathlib.Path(outputPath).absolute()
    manifestPathPath = pathlib.Path(manifestPath).absolute()




    # check if the input and output folders are valid.
    # ------------------------------------------------

    log.out(f'Checking input/output directories...')
    if not inputPathPath.exists():
        raise ValueError(f"Your input folder - {inputPathPath} - is not a real directory.")
    elif inputPathPath.is_file():
        raise ValueError(f"Your input folder - {inputPathPath} - is a file, not a directory.")

    if not outputPathPath.exists():
        raise ValueError(f"Your output folder - {outputPathPath} - is not a real directory.")
    elif outputPathPath.is_file():
        raise ValueError(f"Your output folder - {outputPathPath} - is a file, not a directory.")

    if not manifestPathPath.exists():
        raise ValueError(f"Your manifest - {manifestPathPath} - is not a real directory.")
    elif manifestPathPath.is_dir():
        raise ValueError(f"Your manifest - {manifestPathPath} - is a directory, not a file.")


    log.out(f'Input/output directories verified.', 32)




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

    log.out(f'Output format(s) verified.', 32)




    # check the image sets for each format.
    # ------------------------------------------------

    log.out(f'Checking + getting glyph images...')
    glyphs = getGlyphs(inputPathPath, delim, glyphImageFormats, no_lig, no_vs16, nsc)

    log.out(f'Glyphs acquired.', 32)



    # try to load and check the manifest.
    # ------------------------------------------------

    log.out(f'Loading manifest JSON...')
    try:
        with open(manifestPath, "r") as read_file:
            manifest = json.load(read_file)
    except Exception as e:
        raise Exception('Loading the manifest file failed!' + str(e))

    log.out(f'Manifest loaded.', 32)


    # assemble each font format.
    # ------------------------------------------------

    log.out(f'Begin font compilation!', 35)

    for f in outputFormats:
        createFont(f, outputPath, manifest, glyphs, ttx_output, dev_ttx_output)

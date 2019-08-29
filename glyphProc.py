import pathlib

import log
from glyph import simpleHex, Glyph, Img

# glyphProc.py
# -----------------------------
#
# processing and compiling glyphs before font creation.


def compileImageGlyphs(dir, m, delim, nusc, afsc, imageFormats):

    ## get a rough list of everything

    imgCollection = dict()

    if 'svg' in imageFormats:

        if not (dir / 'svg').exists():
            raise Exception(f"You don't have an 'svg' folder in your input!")

        if not list((dir / 'svg').glob("*.svg")):
            raise Exception(f"There are no svg images in your SVG folder!.")

        imgCollection['svg'] = dict()

        for path in list((dir / 'svg').glob("*.svg")):
            imgCollection['svg'][path.stem] = Img("svg", 0, m, path.absolute(), afsc)



    if 'png' in imageFormats:

        if not list(dir.glob("png*")):
            raise Exception(f"There are no PNG folders in your input folder.")

        for pngFolder in list(dir.glob("png*")):
            if not pngFolder.name[0] == '.' and not pngFolder.suffix: # if it's not a hidden file and if it's not a file.

                try:
                    formatName, strike = pngFolder.name.split('-', 2)
                    strikeSize = int(strike)
                except ValueError as e:
                    raise Exception(f"One of your PNG folders ('{pngFolder.name}') isn't named properly. Make sure it's 'png-<strike size>'.")

                if not list(pngFolder.glob("*.png")):
                    raise Exception(f"There are no PNG images in '{pngFolder}'.")

                imgCollection[pngFolder.name] = dict()

                for path in list(pngFolder.glob("*.png")):
                    imgCollection[pngFolder.name][path.stem] = Img("png", strikeSize, m, path.absolute())


    ## check size

    firstFolderName = list(imgCollection.keys())[0]
    firstFolder = imgCollection[firstFolderName]

    if len(imgCollection) > 1:
        for key, folder in list(imgCollection.items())[1:]:
            if not len(folder) == len(firstFolder):
                raise Exception(f"The amount of glyphs in your input folders aren't the same. '{key}' has {str(len(folder))}. '{firstFolderName}' has {len(firstFolder)}. The amount of images in every folder should be the same.")



    ## convert them into glyphs
    ## (at the same time checking if all the codepoint names are the same)

    imgGlyphs = []

    for c, file in firstFolder.items():
        imgDict = dict()

        for folderName, folder in imgCollection.items():
            if not c in folder:
                raise Exception(f"There's a mismatch in your files. I tried to find an image for the codepoint '{c}' in '{folderName}', but I couldn't find one. You have to make sure you have the exact same sets of filenames in each of your input folders.")
            else:
                imgDict[folderName] = folder[c]

        try:
            imgGlyphs.append(Glyph(c, imgDict=imgDict, delim=delim))
        except ValueError as e:
            raise Exception(f"There was a problem when trying to create a glyph object for {c}. → {e}")


    return imgGlyphs






def compileAliasGlyphs(glyphs, aliases, delim):

    # basic check!

    for target, destination in aliases.items():

        try:
            aliasGlyph = Glyph(target, alias=destination, delim=delim)
        except ValueError as e:
            raise Exception(f"Some part of an alias glyph isn't named correctly. → {e}")


        # is the target NOT a real destination
        targetMatches = False

        for g in glyphs:
            if aliasGlyph == g:
                targetMatches = True

        if targetMatches:
            raise Exception(f"The codepoint sequence for the alias glyph ('{target}') is represented in your image glyphs. It has to be something different.")


        # is the destination is a real destination
        destinationMatches = False

        for g in glyphs:
            if aliasGlyph.alias == g.codepoints:
                destinationMatches = True

        if not destinationMatches:
            raise Exception(f"The destination ('{destination}') of the alias glyph '{target}' is not represented in your image glyphs.")

        glyphs.append(aliasGlyph)


    return glyphs



def addServiceGlyphs(glyphs, no_vs16):
    """
    adds service glyphs to the list of glyphs based on various requirements.
    """

    newGlyphs = []

    vs16Presence = False
    zwjPresence = False

    for g in glyphs:

        # presence
        if g.codepoints.vs16 and no_vs16 is False: vs16Presence = True
        if 0x200d in g.codepoints.seq: zwjPresence = True


    # add particular service glyphs.

    glyphs.append(Glyph(["20"], userInput=False)) # breaking space
    glyphs.append(Glyph(["a0"], userInput=False)) # non-breaking space
    if vs16Presence: glyphs.append(Glyph(["fe0f"], userInput=False))
    if zwjPresence: glyphs.append(Glyph(["200d"], userInput=False))


    return glyphs




def glyphDuplicateTest(glyphs):
    """
    Checks whether there are any duplicates in codepoints in a list of glyphs.
    """
    for id1, g1 in enumerate(glyphs):
        for id2, g2 in enumerate(glyphs):
            if g1 == g2:
                if id1 != id2:
                    raise Exception(f"One of your glyphs (image paths - {g1.img}) when processed, becomes {g1}. This matches another glyph that you have - {g2}. Make sure that your codepoint sequences aren't duplicates when stripped of VS16s (fe0f).")




def areGlyphLigaturesSafe(glyphs):

    singleGlyphCodepoints = []
    ligatures = []

    for g in glyphs:
        if len(g.codepoints) > 1:
            ligatures.append(g)
        else:
            singleGlyphCodepoints.append(g.codepoints.seq[0])

    for g in ligatures:
        for codepoint in g.codepoints.seq:
            if codepoint not in singleGlyphCodepoints:
                raise Exception(f"One of your ligatures ({g.codepoints}) has an individual codepoint (apart from fe0f and 200d) that is not represented as a glyph itself ({simpleHex(codepoint)}). All components of all ligatures (apart from fe0f and 200d) must be represented as glyphs.")




def mixAndSortGlyphs(glyphs):

    glyphStruct = {"all": [], "img_empty": [], "img": [], "empty": []}


    # sort glyphs.
    #
    # (using the glyphs' internal sorting mechanism, which sorts by
    # codepoint sequence length, then the value of the first codepoint.)
    #
    # THIS IS INCREDIBLY CRUCIAL AND CANNOT BE SKIPPED.
    #
    # CHECK OUT THE CODEPOINTSEQ CLASS TO UNDERSTAND WHY.

    glyphs.sort()

    for g in glyphs:

        glyphStruct["all"].append(g)

        if g.glyphType is not "alias":
            glyphStruct["img_empty"].append(g)

        if g.glyphType is "img":
            glyphStruct["img"].append(g)

        if g.glyphType is "empty":
            glyphStruct["empty"].append(g)


    return glyphStruct





def getGlyphs(inputPath, m, aliases, delim, imageFormats, flags):
    """
    Runs inputs through all of the necessary processes and checks to create a glyphs structure.
    """

    # compile image glyphs
    log.out(f'- Getting + validating image glyphs... (this can take a while)', 90)
    imgGlyphs = compileImageGlyphs(inputPath, m, delim, flags["nusc"], flags["afsc"], imageFormats)


    # compile alias glyphs
    if aliases:
        log.out(f'- Getting + validating alias glyphs...', 90)
        glyphs = compileAliasGlyphs(imgGlyphs, aliases, delim)
    else:
        glyphs = imgGlyphs


    # process service glyphs
    log.out(f'- Adding service codepoints...', 90)
    glyphs = addServiceGlyphs(glyphs, flags["no_vs16"])


    # check for duplicate codepoints without VS16
    if not flags["no_vs16"]:
        log.out(f'- Checking if there are any duplicate glyphs...', 90)
        glyphDuplicateTest(glyphs)


    # validating (or stripping) ligatures
    if flags["no_lig"]:
        log.out(f'- [--no-lig] Stripping any ligatures...', 90)
        singleGlyphs = []

        for g in glyphs:
            if len(g.codepoints) == 1:
                singleGlyphs.append(g)

        glyphs = singleGlyphs

    else:
        log.out(f'- Validating ligatures...', 90)
        areGlyphLigaturesSafe(glyphs)


    log.out(f'- Mixing and sorting glyphs...', 90)
    return mixAndSortGlyphs(glyphs)

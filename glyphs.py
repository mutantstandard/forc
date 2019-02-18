import pathlib

import log



def glyphName(int):
    return (hex(int)[2:])




class glyph:

    def __init__(self, codepoints, name, imagePath=None, vs16=False):

        if codepoints:
            self.codepoints = codepoints
        elif imagePath:
            self.codepoints = [int(hex, 16) for hex in imagePath.stem.split(delim_codepoint)]
        else:
            raise ValueError(f"Tried to make glyph object '{name}' but doesn't have a codepoint AND it doesn't have an image path.")

        if name:
            self.name = name
        else:
            self.name = 'u' + '_'.join(map(glyphName, codepoints))

        self.imagePath = imagePath
        self.vs16 = vs16




    def __str__(self):
        return f"{self.name}"


    def __repr__(self):
        return self.__str__()



def getImagesFromDir(dir, formats):

    glyphSet = dict()

    if 'svg' in formats:
        svgFolders = list(dir.glob("svg"))

        if not svgFolders:
            raise Exception(f"You don't have an SVG folder in your input!")


        svgImagePaths = list(svgFolders[0].glob("*.svg"))

        if not svgImagePaths:
            raise Exception(f"There are no SVG images in your SVG folder!.")
        else:
            glyphSet['svg'] = svgImagePaths


    if 'png' in formats:

        # checking if there are PNG folders and if they're named correctly.
        pngFolders = dict()

        for item in list(dir.glob("png*")):
            if not item.name[0] == '.': # if it's not a hidden file.
                if not item.suffix: # if it's not a file.

                    if len(item.name.split('-')) < 2:
                        raise Exception(f"One of your PNG strikes ('{item.name}') is not formatted properly.")
                    else:
                        strikeNum = item.name.split('-')[1]

                    if not strikeNum.isdigit():
                        raise Exception(f"One of your PNG strikes ('{item.name}') doesn't have a number at the end.")
                    else:
                        pngFolders[item.name] = item

        if not pngFolders:
            raise Exception(f"You're exporting to PNG-based font formats but you don't have any PNG subfolders in your input folder.")



        # check if there are images in each strike and get them if they are.

        for name, strike in pngFolders.items():
            pngImagePaths = list(strike.glob("*.png"))

            if not pngImagePaths:
                raise Exception(f"There are no PNG images in '{strike.name}'.")
            else:
                glyphSet[strike.name] = pngImagePaths


    return glyphSet






def areGlyphImagesConsistent(glyphSet):

    if len(glyphSet) > 1:

        # get one of the subfolders and use it as a basis for comparison.

        firstSubfolderName = list(glyphSet.keys())[0]
        firstSubfolder = glyphSet[firstSubfolderName]
        firstSubfolderLength = len(firstSubfolder)



        # check that every subfolder has the same amount of glyhs.
        # ------------------------------------------------------
        for key, subfolder in glyphSet.items():
            if not key == firstSubfolderName:
                if not len(subfolder) == firstSubfolderLength:
                    raise Exception(f"The amount of glyphs in your input subfolders don't match. Subfolder '{key}' has {str(len(subfolder))}. The first subfolder I looked at ({firstSubfolderName}) has {firstSubfolderLength}.")



        # check that every subfolder has the same contents.
        # ------------------------------------------------------

        # iterate over every image in the folder being used as the basis.
        for image in firstSubfolder:

            # iterate over every subfolder (apart from the basis one)
            for key, subfolder in glyphSet.items():
                if not key == firstSubfolderName:

                    subfolderMatches = []

                    # see if there's an image in each subfolder that matches.
                    for comparedImageFile in subfolder:
                        if image.stem == comparedImageFile.stem:
                            subfolderMatches.append(comparedImageFile)

                    if not subfolderMatches:
                        raise Exception(f"The contents of your input subfolders don't match. Subfolder '{firstSubfolderName}' has {image.stem}, but I couldn't find the same file in subfolder '{key}'.")






def compileGlyphData(dir, delim_codepoint, no_vs16, glyphImageSet):


    # start glyphs
    # --------------------------------------------------------------------

    firstSubfolderName = list(glyphImageSet.keys())[0]
    firstSubfolder = glyphImageSet[firstSubfolderName]

    glyphs = []

    vs16Allowed = not no_vs16

    # only add space. do not add characters below 0x20.
    glyphs.append(glyph([0x20], 'space', None))



    # process and check all of the input glyph codepoints
    # --------------------------------------------------------------------

    vs16Presence = False
    zwjPresence = False

    for i in firstSubfolder:
        codepoints = []

        # try to check if every part of the
        # filename stem is a valid hexadecimal number.

        try:
            codepoints = [int(hex, 16) for hex in i.stem.split(delim_codepoint)]

        except ValueError as e:
            log.out(f'!!! One of your glyphs is not named as hexadecimal numbers. It is \'{i.name}\'.', 31)


        for c in codepoints:
            if c < int('20', 16):
                raise Exception(f"A codepoint in one of your glyphs ('{i}') is below U+20. You cannot encode glyphs below this number because various typing environments get confused when you do.")

            if c == int('20', 16):
                raise Exception(f"A codepoint in one of your glyphs ('{i}') is U+20. This is space - you shouldn't be using a glyph here.")

        # compile a glyph file structure.

        structPaths = dict()

        for subfolderName, subfolders in glyphImageSet.items():

            filename = i.stem + "." + subfolderName.split('-')[0]
            structPaths[subfolderName] = pathlib.Path(dir / subfolderName / filename ).absolute()



        # tidy instances of fe0f before adding them to the glyph list

        if int('fe0f', 16) in codepoints:

            vs16Presence = vs16Allowed
            codepoints.remove(int('fe0f', 16))

            if len(codepoints) == 1:
                glyphs.append(glyph(codepoints, None, structPaths, vs16Allowed))

            else:
                glyphs.append(glyph(codepoints, None, structPaths, False))

        else:
            glyphs.append(glyph(codepoints, None, structPaths, False))

        if int('200d', 16) in codepoints:
            zwjPresence = True


    # Add vs16 to the glyphs if one of the
    # processed codepoint chains contains U+fe0f.

    if vs16Presence:
        glyphs.append(glyph([0xfe0f], 'VS16', None))

    # Add ZWJ to the glyphs if one of the
    # processed codepoint chains contains U+200d.

    if zwjPresence:

        # The glyph.name is 'u200d' because that's how other
        # parts of the app will interpret 200d as a GlyphID.
        # DO NOT CHANGE IT.

        glyphs.append(glyph([0x200d], 'u200d', None))

    return glyphs







def postVS16DupeTest(glyphs):
    for id1, g1 in enumerate(glyphs):
        for id2, g2 in enumerate(glyphs):
            if g1.name == g2.name:
                if id1 != id2:
                    raise Exception(f"One of your glyphs ({g1.imagePath}), when stripped of VS16 (fe0f), matches another ({g2.imagePath}). There can't be duplicates in this scenario.")






def areGlyphLigaturesSafe(glyphs):
    singleGlyphCodepoints = []
    ligatures = []

    #TEMP
    singleGlyphs = []

    for g in glyphs:
        if len(g.codepoints) > 1:
            ligatures.append(g)
        else:
            singleGlyphCodepoints.append(g.codepoints[0])
            singleGlyphs.append(g)


    for g in ligatures:
        for codepoint in g.codepoints:
            if codepoint not in singleGlyphCodepoints:
                raise Exception(f"One of your ligatures ({g.imagePath}) does not have all non-service codepoints represented as glyphs ({glyphName(codepoint)}). All components of all ligatures must be represented as glyphs (apart from fe0f and 200d).")











def getGlyphs(inputPath, delim_codepoint, formats, no_lig, no_vs16, nfcc):
    """
    - Validates glyph image paths from the input path.
    - Returns a list of glyph objects, including important special control glyphs.
    """

    log.out(f'Checking + getting file paths...', 90)
    glyphImageSet = getImagesFromDir(inputPath, formats)


    if not nfcc:
        log.out(f'Checking file consistency...', 90)
        areGlyphImagesConsistent(glyphImageSet)


    log.out(f'Compiling glyph data...', 90)
    glyphs = compileGlyphData(inputPath, delim_codepoint, no_vs16, glyphImageSet)


    log.out(f'Validating glyph data...', 90)
    postVS16DupeTest(glyphs)


    if no_lig:
        log.out(f'Stripping any ligatures...', 90)
        singleGlyphs = []

        for g in glyphs:
            if len(g.codepoints) == 1:
                singleGlyphs.append(g)

        return singleGlyphs

    else:
        log.out(f'Validating ligatures...', 90)
        areGlyphLigaturesSafe(glyphs)
        return glyphs

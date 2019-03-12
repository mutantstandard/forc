import pathlib

import log
from validate.svg import isSVGValid


def glyphName(int):
    return (hex(int)[2:])




class glyph:

    def __init__(self, codepoints, imagePath=None, vs16=False):

        if codepoints:
            self.codepoints = codepoints
        elif imagePath:
            self.codepoints = [int(hex, 16) for hex in imagePath.stem.split(delim_codepoint)]
        else:
            raise ValueError(f"Tried to make glyph object '{name}' but doesn't have a codepoint AND it doesn't have an image path.")

        self.name = 'u' + '_'.join(map(glyphName, codepoints))
        self.imagePath = imagePath
        self.vs16 = vs16




    def __str__(self):
        return f"{self.name}"


    def __repr__(self):
        return self.__str__()


    def __eq__(self, other):
        return self.codepoints == other.codepoints


    def __lt__(self, other):
        if len(self.codepoints) < len(other.codepoints):
            return True
        elif len(self.codepoints) == len(other.codepoints):
            return self.codepoints < other.codepoints
        return False

    def __len__(self):
        return len(self.codepoints)








def getImagesFromDir(dir, formats):

    glyphSet = dict()

    if 'svg' in formats:

        # try to get a SVG Folder
        svgFolders = list(dir.glob("svg"))

        if not svgFolders:
            raise Exception(f"You don't have an SVG folder in your input!")

        # get a list of all SVG files in the SVG folder.
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




def validateCodepoint(c, i):
    """
    Make sure a particular user-inputted codepoint string is within the right ranges.
    Throws an exception when it is not.
    """
    if c < int('20', 16):
        raise Exception(f"One of your glyphs ('{i.stem}') contains a codepoint that is below U+20. You cannot encode glyphs below this number because various typing environments get confused when you do.")

    if c == int('20', 16):
        raise Exception(f"One of your glyphs ('{i.stem}') contains U+20. This is space - you shouldn't be using a glyph for this.")

    if c == int('a0', 16):
        raise Exception(f"One of your glyphs ('{i.stem}') contains U+a0. This is a space character - you shouldn't be using a glyph for this.")

    if c > int('10FFFF', 16):
        raise Exception(f"One of your glyphs ('{i.stem}') contains a codepoint that is above U+10FFFF. The Unicode Standard currently does not support codepoints above this number.")





def compileGlyphData(dir, delim_codepoint, no_vs16, glyphImageSet):
    """
    Compiles a glyph data structure from a set of glyph images.
    """

    firstSubfolderName = list(glyphImageSet.keys())[0]
    firstSubfolder = glyphImageSet[firstSubfolderName]

    glyphs = []

    vs16Allowed = not no_vs16

    vs16Presence = False
    zwjPresence = False



    # (iterating over one subfolder because the other subfolders
    # have already been verified as identical.)

    for i in firstSubfolder:
        codepoints = []



        # try to convert the filename into a string of hexadecimal numbers
        try:
            codepoints = [int(hex, 16) for hex in i.stem.split(delim_codepoint)]
        except ValueError as e:
            log.out(f"!!! One of your glyphs ('{i.name}') is not named as a hexidecimal number or a series of hexadecimal numbers.", 31)


        # make sure each inputted codepoint is in an appropriate range.
        for c in codepoints:
            validateCodepoint(c, i)


        # compile a dictionary containing all of the different image formats for this glyph.
        structPaths = dict()

        for subfolderName, subfolders in glyphImageSet.items():
            filename = i.stem + "." + subfolderName.split('-')[0]
            structPaths[subfolderName] = pathlib.Path(dir / subfolderName / filename ).absolute()


        # test for presence of ZWJs
        if int('200d', 16) in codepoints:
            zwjPresence = True

        # TODO: validate ZWJ placement.

        # tidy instances of fe0f before adding them to the glyph list:
        fe0f = int('fe0f', 16)
        strippedCodepoints = [c for c in codepoints if c != fe0f]
        vs16Enabled = vs16Allowed and fe0f in codepoints and len(strippedCodepoints) == 1
        glyphs.append(glyph(strippedCodepoints, structPaths, vs16Enabled))





    # add particular service glyphs based on user input.

    glyphs.append(glyph([0x20], None)) # breaking space
    glyphs.append(glyph([0xa0], None)) # non-breaking space

    if vs16Presence: glyphs.append(glyph([0xfe0f], None))
    if zwjPresence: glyphs.append(glyph([0x200d], None))




    # sort glyphs from lowest codepoints to highest.
    #
    # THIS IS REALLY IMPORTANT BECAUSE IT DETERMINES THE GLYPHID
    #
    # IF CERTAIN LOW-NUMBER CHARACTERS HAVE GLYPHIDS OUR OF THEIR
    # PARTICULAR HEXADECIMAL RANGES, IT WONT COMPILE.

    glyphs.sort()


    return glyphs











def glyphDuplicateTest(glyphs):
    """
    Checks whether there are any duplicates in codepoints in a list of glyphs.
    """
    for id1, g1 in enumerate(glyphs):
        for id2, g2 in enumerate(glyphs):
            if g1 == g2:
                if id1 != id2:
                    raise Exception(f"One of your glyphs ({g1.imagePath}), when stripped of VS16 (fe0f), matches another ({g2.imagePath}). There can't be duplicates in this scenario.")




def validateImageData(glyphs, nusc):
    for g in glyphs:
        if g.imagePath:
            if g.imagePath['svg']:
                isSVGValid(g, ignoreUnenforcedContents=nusc)




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







def getGlyphs(inputPath, delim_codepoint, formats, no_lig, no_vs16, nusc, nfcc):
    """
    - Validates glyph image paths from the input path.
    - Returns a list of glyph objects, including important special control glyphs.
    """


    # check the input directory structure and get the images that are in there
    log.out(f'Checking + getting file paths...', 90)
    glyphImageSet = getImagesFromDir(inputPath, formats)


    # check the consistency of the codepoints declared in the glyph images
    # (or not)
    if not nfcc:
        log.out(f'Checking file consistency...', 90)
        areGlyphImagesConsistent(glyphImageSet)


    # compile glyph data
    log.out(f'Compiling glyph data...', 90)
    glyphs = compileGlyphData(inputPath, delim_codepoint, no_vs16, glyphImageSet)


    # check for duplicate codepoints without VS16
    log.out(f'Checking if there are any duplicate codepoints when ignoring VS16...', 90)
    glyphDuplicateTest(glyphs)


    # check image data
    log.out(f'Validating image data...', 90)
    validateImageData(glyphs, nusc)


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

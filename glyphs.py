import pathlib

import log
from validate.svg import isSVGValid
from validate.codepoints import testZWJSanity, testRestrictedCodepoints
from utils.codepoints import codepointSeq, glyphName





class glyph:

    def __init__(self, codepoints, imagePath=None, vs16=False, alias=None):

        if codepoints:
            self.codepoints = codepoints
        elif imagePath:
            self.codepoints = [int(hex, 16) for hex in imagePath.stem.split(delim_codepoint)]
        else:
            raise ValueError(f"Tried to make glyph object '{name}' but doesn't have a codepoint AND it doesn't have an image path.")


        if alias:
            if not imagePath:
                self.aliasName = glyphName(alias)
            else:
                raise ValueError(f"Tried to make glyph object '{name}' but it is set as an alias AND has an image path. It can't have both.")

        self.name = glyphName(self.codepoints)
        self.imagePath = imagePath
        self.vs16 = vs16
        self.alias = alias


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

    def resetName(self):
        self.name = glyphName(self.codepoints)

    def resetAliasName(self):
        self.aliasName = glyphName(self.alias)




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







def compileImageGlyphs(dir, delim_codepoint, no_vs16, glyphImageSet):
    """
    Compiles a list of image glyphs from a set of glyph images.
    """

    firstSubfolderName = list(glyphImageSet.keys())[0]
    firstSubfolder = glyphImageSet[firstSubfolderName]

    glyphs = []


    # (iterating over one subfolder because the other subfolders
    # have already been verified as identical.)

    for i in firstSubfolder:
        # try to convert the filename into a string of hexadecimal numbers
        try:
            codepoints = codepointSeq(i.stem, delim_codepoint)
        except ValueError as e:
            raise Exception(f"One of your image glyphs ('{i.name}') is not named correctly. ({e})", 31)


        # compile a dictionary containing all of the different image formats for this glyph.
        imagePath = dict()

        for subfolderName, subfolders in glyphImageSet.items():
            filename = i.stem + "." + subfolderName.split('-')[0]
            imagePath[subfolderName] = pathlib.Path(dir / subfolderName / filename ).absolute()


        # finally add the codepoint to the glyph list.
        glyphs.append(glyph(codepoints, imagePath))


    return glyphs







def compileAliasGlyphs(glyphs, aliases, delim_codepoint):


    # basic check!

    for target, destination in aliases.items():

        # TARGET
        # -----------------


        # is the target a real sequence
        try:
            targSeq = codepointSeq(target, delim_codepoint)
        except ValueError as e:
            raise Exception(f"The alias glyph '{target}' is not named correctly. ({e})", 31)


        # is the target NOT a real destination
        targetMatches = False

        for g in glyphs:
            if targSeq == g.codepoints:
                targetMatches = True

        if targetMatches:
            raise Exception(f"The codepoint sequence for the alias glyph ('{target}') is represented in your image glyphs. It has to be something different.", 31)



        # DESTINATION
        # -----------------


        # is the destination is a real sequence
        try:
            destSeq = codepointSeq(destination, delim_codepoint)
        except ValueError as e:
            raise Exception(f"The destination ('{destination}') of the alias glyph '{target}' is not named correctly. ({e})", 31)


        # is the destination is a real destination
        destinationMatches = False

        for g in glyphs:
            if destSeq == g.codepoints:
                destinationMatches = True

        if not destinationMatches:
            raise Exception(f"The destination ('{destination}') of the alias glyph '{target}' is not represented in your image glyphs.", 31)

        glyphs.append(glyph(targSeq, alias=destSeq))


    return glyphs




def serviceGlyphProc(glyphs, no_vs16):

    newGlyphs = []
    vs16Allowed = not no_vs16

    vs16Presence = False
    zwjPresence = False

    for g in glyphs:

        # TEST FOR INAPPROPRIATE CODEPOINTS
        # -------------------------------------
        # make sure each inputted codepoint is in an appropriate range.
        testRestrictedCodepoints(g.codepoints, g.name)

        # VS16
        # -------------
        fe0f = int('fe0f', 16)

        # strip instances of fe0f
        g.codepoints = [c for c in g.codepoints if c != fe0f]

        # set vs16Enabled to True if it fits the right parameters.
        g.vs16Enabled = vs16Allowed and fe0f in g.codepoints and len(g.codepoints) == 1


        # ZWJ
        # -------------
        # test and validate presence of ZWJs
        zwj = int('200d', 16)

        if zwj in g.codepoints:
            zwjPresence = True
            testZWJSanity(g.codepoints, g.name)

        g.resetName()


        if g.alias:

            g.alias = [c for c in g.alias if c != fe0f]

            if zwj in g.alias:
                testZWJSanity(g.alias, g.name)

            g.resetAliasName()



    # add particular service glyphs based on user input.

    glyphs.append(glyph([0x20])) # breaking space
    glyphs.append(glyph([0xa0])) # non-breaking space

    if vs16Presence: glyphs.append(glyph([0xfe0f]))
    if zwjPresence: glyphs.append(glyph([0x200d]))


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




def mixAndSortGlyphs(glyphs):

    glyphStruct = dict()

    glyphStruct["all"] = []
    glyphStruct["img"] = []

    for g in glyphs:
        if not g.alias:
            glyphStruct["all"].append(g)
            glyphStruct["img"].append(g)
        else:
            glyphStruct["all"].append(g)

    # sort glyphs from lowest codepoints to highest.
    #
    # THIS IS REALLY IMPORTANT BECAUSE IT DETERMINES THE GLYPHID
    #
    # IF CERTAIN LOW-NUMBER CHARACTERS HAVE GLYPHIDS OUR OF THEIR
    # PARTICULAR HEXADECIMAL RANGES, IT WONT COMPILE.

    glyphStruct["all"].sort()
    glyphStruct["img"].sort()

    return glyphStruct





def getGlyphs(inputPath, aliases, delim_codepoint, formats, no_lig, no_vs16, nusc, nfcc):
    """
    - Validates glyph image paths from the input path.
    - Returns a list of glyph objects, including important special control glyphs.
    """


    # check the input directory structure and get the images that are in there
    log.out(f'Checking + getting image glyph file paths...', 90)
    glyphImageSet = getImagesFromDir(inputPath, formats)


    # check the consistency of the codepoints declared in the glyph images
    # (or not)
    if not nfcc:
        log.out(f'Checking image glyph file consistency...', 90)
        areGlyphImagesConsistent(glyphImageSet)


    # compile image glyphs
    log.out(f'Compiling + validating image glyphs...', 90)
    glyphs = compileImageGlyphs(inputPath, delim_codepoint, no_vs16, glyphImageSet)


    # compile alias glyphs
    if aliases:
        log.out(f'Compiling + validating alias glyphs...', 90)
        glyphs = compileAliasGlyphs(glyphs, aliases, delim_codepoint)


    # process service glyphs
    log.out(f'Processing service glyphs...', 90)
    glyphs = serviceGlyphProc(glyphs, no_vs16)


    # check for duplicate codepoints without VS16
    if not no_vs16:
        log.out(f'Checking if there are any duplicate image glyphs when ignoring VS16...', 90)
        glyphDuplicateTest(glyphs)


    # check image data
    log.out(f'Validating image glyph image data...', 90)
    validateImageData(glyphs, nusc)


    # validating (or stripping) ligatures
    if no_lig:
        log.out(f'Stripping any ligatures...', 90)
        singleGlyphs = []

        for g in glyphs:
            if len(g.codepoints) == 1:
                singleGlyphs.append(g)

        glyphs = singleGlyphs

    else:
        log.out(f'Validating ligatures...', 90)
        areGlyphLigaturesSafe(glyphs)

    log.out(f'Mixing and sorting glyphs...', 90)
    return mixAndSortGlyphs(glyphs)

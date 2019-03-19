import pathlib

import log
from validate.svg import isSVGValid
from validate.codepoints import testZWJSanity, testRestrictedCodepoints



def simpleHex(int):
    """
    returns a hexadecimal number as a string without the '0x' prefix.
    """

    return (hex(int)[2:])


class codepointSeq:

    def __init__(self, sequence, delim):

        if type(sequence) is str:
            try:
                self.seq = [int(c, 16) for c in sequence.split(delim)]
            except ValueError as e:
                raise ValueError("Codepoint sequence isn't named correctly. Make sure your codepoint sequence consists only of hexadecimal numbers and are separated by the right delimiter.")

        elif type(sequence) is list:
            try:
                seq = [int(c, 16) for c in sequence]
            except ValueError as e:
                raise ValueError("Codepoint sequence isn't named correctly. Make sure each component of your list is a hexadecimal number.")

            self.seq = seq


    def name(self):
        return 'u' + '_'.join(map(simpleHex, self.seq))

    def __str__(self):
        return self.name()

    def __repr__(self):
        return self.name()

    def __eq__(self, other):
        return self.seq == other.seq

    def __lt__(self, other):
        if len(self.seq) < len(other.seq):
            return True
        elif len(self.seq) == len(other.seq):
            return self.seq < other.seq
        return False

    def __len__(self):
        return len(self.seq)

    def __str__(self):
        return str(self.seq)




class glyph:

    def __init__(self, codepoints, imagePath=None, vs16=False, alias=None, delim="-"):

        try:
            self.codepoints = codepointSeq(codepoints, delim)
        except ValueError as e:
            raise Exception(f"The glyph ('{codepoints}') is not named correctly. ({e})", 31)


        if alias is None:
            self.alias = None
        else:
            if imagePath:
                raise ValueError(f"Tried to make glyph object '{name}' but it is set as an alias AND has an image path. It can't have both.")
            else:
                try:
                    self.alias = codepointSeq(alias, delim)
                except ValueError as e:
                    raise Exception(f"The alias destination ('{alias}') for {self.codepoints} is not named correctly. ({e})", 31)


        self.imagePath = imagePath
        self.vs16 = vs16


    def __str__(self):
        return self.codepoints.name()

    def __repr__(self):
        return self.codepoints.name()

    def __eq__(self, other):
        return self.codepoints == other.codepoints

    def __lt__(self, other):
        return self.codepoints < other.codepoints

    def __len__(self):
        return len(self.codepoints)






def compileImageGlyphs(dir, delim, nusc, formats):

    ## get a rough list of everything

    imgSet = dict()

    if 'svg' in formats:

        if not (dir / 'svg').exists():
            raise Exception(f"You don't have an 'svg' folder in your input!")

        imgSet['svg'] = list((dir / 'svg').glob("*.svg"))

        if not imgSet["svg"]:
            raise Exception(f"There are no svg images in your SVG folder!.")

        for svg in imgSet['svg']:
            isSVGValid(svg, nusc)


    if 'png' in formats:

        if not list(dir.glob("png*")):
            raise Exception(f"There are no PNG folders in your input folder.")

        for pngFolder in list(dir.glob("png*")):
            if not pngFolder.name[0] == '.': # if it's not a hidden file. TODO: replace with something simpler
                if not pngFolder.suffix: # if it's not a file. #TODO: replace with something simpler

                    try:
                        formatName, strike = pngFolder.name.split('-', 2)
                        strikeSize = int(strike)
                    except ValueError as e:
                        raise Exception(f"One of your PNG strikes ('{item.name}') isn't named properly.")

                    imgSet[pngFolder.name] = list(pngFolder.glob("*.png"))

                    if not imgSet[pngFolder.name]:
                        raise Exception(f"There are no PNG images in '{pngFolder}'.")



    ## check the length of every subfolder to see if they match.

    firstSubfolderName = list(imgSet.keys())[0]
    firstSubfolder = imgSet[firstSubfolderName]

    if len(imgSet) > 1:
        for key, subfolder in list(imgSet.items())[1:]:
            if not len(subfolder) == len(firstSubfolder):
                raise Exception(f"The amount of glyphs in your input subfolders don't match. Subfolder '{key}' has {str(len(subfolder))}. The first subfolder I looked at ({firstSubfolderName}) has {firstSubfolderLength}.")



    ## convert them into glyphs

    imgGlyphs = []

    for i in firstSubfolder:
        imagePath = dict()

        for subfolderName, subfolders in imgSet.items():
            filename = i.stem + "." + subfolderName.split('-')[0]
            imagePath[subfolderName] = pathlib.Path(dir / subfolderName / filename ).absolute()

        # finally add the codepoint to the glyph list.
        try:
            imgGlyphs.append(glyph(i.stem, imagePath, delim))
        except ValueError as e:
            raise Exception(f"One of your image glyphs ('{i.name}') is not named correctly. ({e})", 31)



    return imgGlyphs






def compileAliasGlyphs(glyphs, aliases, delim):

    # basic check!

    for target, destination in aliases.items():

        try:
            aliasGlyph = glyph(target, alias=destination, delim=delim)
        except ValueError as e:
            raise Exception(f"Some part of one of your aliases aren't named correctly. {e}")


        # is the target NOT a real destination
        targetMatches = False

        for g in glyphs:
            if aliasGlyph == g:
                targetMatches = True

        if targetMatches:
            raise Exception(f"The codepoint sequence for the alias glyph ('{target}') is represented in your image glyphs. It has to be something different.", 31)


        # is the destination is a real destination
        destinationMatches = False

        for g in glyphs:
            if aliasGlyph.alias == g.codepoints:
                destinationMatches = True

        if not destinationMatches:
            raise Exception(f"The destination ('{destination}') of the alias glyph '{target}' is not represented in your image glyphs.", 31)

        glyphs.append(aliasGlyph)


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
        testRestrictedCodepoints(g)

        # VS16
        # -------------
        fe0f = int('fe0f', 16)

        # strip instances of fe0f
        g.codepoints.seq = [c for c in g.codepoints.seq if c != fe0f]

        # set vs16Enabled to True if it fits the right parameters.
        g.vs16Enabled = vs16Allowed and fe0f in g.codepoints.seq and len(g.codepoints.seq) == 1


        # ZWJ
        # -------------
        # test and validate presence of ZWJs
        zwj = int('200d', 16)

        if zwj in g.codepoints.seq:
            zwjPresence = True
            testZWJSanity(g)


        if g.alias:
            g.alias.seq = [c for c in g.alias.seq if c != fe0f]

            if zwj in g.alias.seq:
                testZWJSanity(g)



    # add particular service glyphs based on user input.

    glyphs.append(glyph(["20"])) # breaking space
    glyphs.append(glyph(["a0"])) # non-breaking space

    if vs16Presence: glyphs.append(glyph(["fe0f"]))
    if zwjPresence: glyphs.append(glyph(["200d"]))


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
                raise Exception(f"One of your ligatures ({g.codepoint.name()}) does not have all non-service codepoints represented as glyphs ({simpleHex(codepoint)}). All components of all ligatures must be represented as glyphs (apart from fe0f and 200d).")




def mixAndSortGlyphs(glyphs):

    glyphStruct = {"all": [], "img": []}

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





def getGlyphs(inputPath, aliases, delim, formats, no_lig, no_vs16, nusc):
    """
    - Validates glyph image paths from the input path.
    - Returns a list of glyph objects, including important special control glyphs.
    """

    # compile image glyphs
    log.out(f'Compiling + validating image glyphs...', 90)
    imgGlyphs = compileImageGlyphs(inputPath, delim, nusc, formats)


    # compile alias glyphs
    if aliases:
        log.out(f'Compiling + validating alias glyphs...', 90)
        glyphs = compileAliasGlyphs(imgGlyphs, aliases, delim)
    else:
        glyphs = imgGlyphs


    # process service glyphs
    log.out(f'Processing service codepoints...', 90)
    glyphs = serviceGlyphProc(glyphs, no_vs16)


    # check for duplicate codepoints without VS16
    if not no_vs16:
        log.out(f'Checking if there are any duplicate image glyphs when ignoring VS16...', 90)
        glyphDuplicateTest(glyphs)


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

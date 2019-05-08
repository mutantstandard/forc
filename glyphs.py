import pathlib

import log
import lxml.etree as etree

from validate.svg import isSVGValid
from validate.codepoints import testZWJSanity, testRestrictedCodepoints
from transform.svg import compensateSVG


# glyphs.py
# -------------------------------
#
# The entire process of importing, compiling and validating glyphs.




def simpleHex(int):
    """
    returns a hexadecimal number as a string without the '0x' prefix.
    """

    return (hex(int)[2:])



class img:
    """
    Class representing a glyph image.
    """
    def __init__(self, type, strike, m, path, nusc=False, afsc=False):
        if not path.exists():
            raise ValueError(f"Image path '{path}' doesn't exist!'")

        if type == "svg":
            isSVGValid(path, nusc)
            svgImage = etree.parse(path.as_uri())
            self.data = compensateSVG(svgImage, m, afsc)

        if type == "png":
            # with open(path, "rb") as read_file:
                # pngHexdump = read_file.read().hex()
            self.path = path

        self.type = type
        self.strike = strike


    def __str__(self):
        return f"|{self.type}-{str(self.strike)} {self.path.name}|"

    def __repr__(self):
        return str(self)





class codepointSeq:
    """
    Class representing a sequence of Unicode codepoints.
    """


    def __init__(self, sequence, delim, userInput=True):

        # create a suitable structure based on the input type.
        # ------------------------------------------------------
        if type(sequence) is str:
            try:
                seq = [int(c, 16) for c in sequence.split(delim)]
            except ValueError as e:
                raise ValueError("Codepoint sequence isn't named correctly. Make sure your codepoint sequence consists only of hexadecimal numbers and are separated by the right delimiter.")

        elif type(sequence) is list:
            try:
                seq = [int(c, 16) for c in sequence]
            except ValueError as e:
                raise ValueError("Codepoint sequence isn't named correctly. Make sure each component of your list is a hexadecimal number.")


        # handle fe0f
        # ------------------------------------------------------
        if len(seq) > 1:
            self.seq = [c for c in seq if c != 0xfe0f]
            self.vs16 = 0xfe0f in seq and len(self.seq) == 1
        else:
            self.seq = seq
            self.vs16 = False


        # test the codepoints
        # # ------------------------------------------------------
        try:
            if userInput: testRestrictedCodepoints(self.seq)
            testZWJSanity(self.seq)
        except ValueError as e:
            raise ValueError(f"{self.seq} is not a valid codepoint sequence. → {e}")



    def name(self):
        return 'u' + '_'.join(map(simpleHex, self.seq))

    def __str__(self):
        return '-'.join(map(simpleHex, self.seq))

    def __repr__(self):
        return self.str()

    def __eq__(self, other):
        return self.seq == other.seq

    def __lt__(self, other):
        """
        Sorts by codepoint sequence length, then the value of the first codepoint.

        This is incredibly crucial to the functioning of font compilation because
        it determines the glyphID in the glyphOrder table.

        Single codepoint seqs have to be first and they have to be ordered
        lowest to highest because if they aren't, their glyphID can be out
        of range of low-bit cmap subtables. If glyphIDs are out of range of
        cmap subtables like this, the font won't compile.
        """
        if len(self.seq) < len(other.seq):
            return True
        elif len(self.seq) == len(other.seq):
            return self.seq < other.seq
        return False

    def __len__(self):
        return len(self.seq)







class glyph:
    """
    Class representing a font glyph.
    """
    def __init__(self, codepoints, img=None, alias=None, delim="-", userInput=True):

        try:
            self.codepoints = codepointSeq(codepoints, delim, userInput=userInput)
        except ValueError as e:
            raise ValueError(f"The codepoint sequence ('{codepoints}') is not valid. → {e}")


        if alias is None:
            self.alias = None
        else:
            if img:
                raise ValueError(f"Tried to make glyph object '{name}' but it is set as an alias AND has an image path. It can't have both.")
            else:
                try:
                    self.alias = codepointSeq(alias, delim)
                except ValueError as e:
                    raise Exception(f"The alias destination ('{alias}') for {self.codepoints} is not named correctly. → {e}")


        self.img = img


    def __str__(self):
        return str(self.codepoints)

    def __repr__(self):
        return self.str()

    def __eq__(self, other):
        return self.codepoints == other.codepoints

    def __lt__(self, other):
        return self.codepoints < other.codepoints

    def __len__(self):
        return len(self.codepoints)









def compileImageGlyphs(dir, m, delim, nusc, afsc, formats):

    ## get a rough list of everything

    imgCollection = dict()

    if 'svg' in formats:

        if not (dir / 'svg').exists():
            raise Exception(f"You don't have an 'svg' folder in your input!")

        if not list((dir / 'svg').glob("*.svg")):
            raise Exception(f"There are no svg images in your SVG folder!.")

        imgCollection['svg'] = dict()

        for path in list((dir / 'svg').glob("*.svg")):
            imgCollection['svg'][path.stem] = img("svg", 0, m, path.absolute(), afsc)



    if 'png' in formats:

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
                    imgCollection[pngFolder.name][path.stem] = img("png", strikeSize, m, path.absolute())


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
        imgSet = dict()

        for folderName, folder in imgCollection.items():
            if not c in folder:
                raise Exception(f"There's a mismatch in your files. I tried to find an image for the codepoint '{c}' in '{folderName}', but I couldn't find one. You have to make sure you have the exact same sets of filenames in each of your input folders.")
            else:
                imgSet[folderName] = folder[c]

        try:
            imgGlyphs.append(glyph(c, img=imgSet, delim=delim))
        except ValueError as e:
            raise Exception(f"There was a problem when trying to create the glyph for {c}. → {e}")


    return imgGlyphs






def compileAliasGlyphs(glyphs, aliases, delim):

    # basic check!

    for target, destination in aliases.items():

        try:
            aliasGlyph = glyph(target, alias=destination, delim=delim)
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

    glyphs.append(glyph(["20"], userInput=False)) # breaking space
    glyphs.append(glyph(["a0"], userInput=False)) # non-breaking space
    if vs16Presence: glyphs.append(glyph(["fe0f"], userInput=False))
    if zwjPresence: glyphs.append(glyph(["200d"], userInput=False))


    return glyphs




def glyphDuplicateTest(glyphs):
    """
    Checks whether there are any duplicates in codepoints in a list of glyphs.
    """
    for id1, g1 in enumerate(glyphs):
        for id2, g2 in enumerate(glyphs):
            if g1 == g2:
                if id1 != id2:
                    raise Exception(f"One of your glyphs (image paths - {g1.img}) when processed, becomes {g1}. This matches another glyph that you have - {g2}. There can't be duplicates in this scenario.")




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
                raise Exception(f"One of your ligatures ({g.codepoints}) does not have all non-service codepoints represented as glyphs ({simpleHex(codepoint)}). All components of all ligatures must be represented as glyphs (apart from fe0f and 200d).")




def mixAndSortGlyphs(glyphs):

    glyphStruct = {"all": [], "img": []}

    for g in glyphs:
        if not g.alias:
            glyphStruct["all"].append(g)
            glyphStruct["img"].append(g)
        else:
            glyphStruct["all"].append(g)

    # sort glyphs.
    #
    # (using the glyphs' internal sorting mechanism, which sorts by
    # codepoint sequence length, then the value of the first codepoint.)
    #
    # THIS IS INCREDIBLY CRUCIAL AND CANNOT BE SKIPPED.
    #
    # CHECK OUT THE CODEPOINTSEQ CLASS TO UNDERSTAND WHY.

    glyphStruct["all"].sort()
    glyphStruct["img"].sort()

    return glyphStruct





def getGlyphs(inputPath, m, aliases, delim, formats, no_lig, no_vs16, nusc, afsc):
    """
    Runs inputs through all of the necessary processes and checks to create a glyphs structure.
    """

    # compile image glyphs
    log.out(f'Compiling + validating image glyphs... (this can take a while)', 90)
    imgGlyphs = compileImageGlyphs(inputPath, m, delim, nusc, afsc, formats)


    # compile alias glyphs
    if aliases:
        log.out(f'Compiling + validating alias glyphs...', 90)
        glyphs = compileAliasGlyphs(imgGlyphs, aliases, delim)
    else:
        glyphs = imgGlyphs


    # process service glyphs
    log.out(f'Adding service codepoints...', 90)
    glyphs = addServiceGlyphs(glyphs, no_vs16)


    # check for duplicate codepoints without VS16
    if not no_vs16:
        log.out(f'Checking if there are any duplicate glyphs...', 90)
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

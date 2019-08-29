import pathlib

import lxml.etree as etree

from validate.svg import isSVGValid
from validate.codepoints import testZWJSanity, testRestrictedCodepoints
from transform.svg import compensateSVG


# glyph.py
# -------------------------------
#
# The entire process of importing, compiling and validating glyphs.




def simpleHex(int):
    """
    returns a hexadecimal number as a string without the '0x' prefix.
    """

    return f"{int:x}"



class Img:
    """
    Class representing a single glyph image.
    """
    def __init__(self, type, strike, m, path, nusc=False, afsc=False):

        if not path.exists():
            raise ValueError(f"Image object couldn't be built because the path given ('{path}') doesn't exist.'")

        self.type = type
        self.strike = strike

        if type == "svg":

            # try parsing the SVG
            try:
                svgImage = etree.parse(path.as_uri())
            except ValueError:
                raise ValueError(f"Image object couldn't be built because there was a problem in retrieving or processing the image '{path}'. {e}")

            # test for SVG compatibility.
            try:
                isSVGValid(svgImage, nusc)
            except ValueError as e:
                raise ValueError(f"Image object couldn't be built due to compatibility issues with the SVG image '{path}'. → {e}")

            # do all the compensation stuff on it and make it the data.
            self.data = compensateSVG(svgImage, m, afsc)



        if type == "png":
            self.path = path
            # take the PNG and use it for later.


    def getHexDump(self):
        """
        Loads and returns a hexdump of the image object's file on-demand.
        """

        if self.type is "svg":
            raise ValueError(f"Hexdump of an SVG image was attempted. You can't hexdump SVG images in forc.")

        try:
            with open(self.path, "rb") as read_file:
                return read_file.read().hex()
        except ValueError as e:
            raise ValueError(f"Image object {self} couldn't be hexdumped. → {e}")


    def getBytes(self):
        """
        Loads and returns a byte dump of the image object's file on-demand.
        """

        try:
            with open(self.path, "rb") as read_file:
                return read_file.read()
        except ValueError as e:
            raise ValueError(f"Bytes couldn't be retrieved from the file of image object {self}. → {e}")


    def __str__(self):
        return f"img: [{self.type}-{str(self.strike)}] {self.path.name}|"

    def __repr__(self):
        return str(self)





class CodepointSeq:
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
            raise ValueError(f"'{sequence}' is not a valid codepoint sequence. → {e}")



    def name(self):
        """
        Generates a TTX 'name' for the glyph based on it's codepoint sequence.

        The way this is named is important and it makes the TTX compiler happy.
        DO NOT CHANGE IT!

        eg. ['1f44d', '101601']
        -> u1f44d_101601
        """
        return 'u' + '_'.join(map(simpleHex, self.seq))

    def __str__(self):
        return '-'.join(map(simpleHex, self.seq))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.seq == other.seq

    def __lt__(self, other):
        """
        Sorts by codepoint sequence length, then the value of the first codepoint.

        This is incredibly crucial to the functioning of font compilation because
        (once a list of these are sorted) it determines the glyphID in the
        glyphOrder table.

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







class Glyph:
    """
    Class representing a font glyph.
    """
    def __init__(self, codepoints, imgDict=None, alias=None, delim="-", userInput=True):

        try:
            self.codepoints = CodepointSeq(codepoints, delim, userInput=userInput)
        except ValueError as e:
            raise ValueError(f"A codepoint sequence object for ('{codepoints}') couldn't be created. → {e}")


        if alias is None:
            self.alias = None
        else:
            if imgDict:
                raise ValueError(f"Tried to make glyph object '{name}' but it has both an alias AND an image. It can't have both.")
            else:
                try:
                    self.alias = CodepointSeq(alias, delim)
                    self.glyphType = "alias"
                except ValueError as e:
                    raise Exception(f"The alias destination ('{alias}') for {self.codepoints} is not named correctly. → {e}")

        self.imgDict = imgDict

        if imgDict is not None:
            self.glyphType = "img"

        if imgDict is None and alias is None:
            self.glyphType = "empty"


    # the way that glyph classes get compared/equated is
    # simply by their codepointseq.

    def __str__(self):
        return str(self.codepoints)

    def __repr__(self):
        return str(self.codepoints) + f" - {self.glyphType}"

    def __eq__(self, other):
        return self.codepoints == other.codepoints

    def __lt__(self, other):
        return self.codepoints < other.codepoints

    def __len__(self):
        return len(self.codepoints)

    def name(self):
        return self.codepoints.name()

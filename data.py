import re

class tag:
    """
    Class encapsulating an TrueType/OpenType tag.
    """

    def __init__(self, string):
        """
        Initialises a tag based on a string.
        Ensures that a string is compliant with OpenType's tag data type before successful instantiation.

        (https://docs.microsoft.com/en-us/typography/opentype/spec/otff#data-types)
        (Must have exactly 4 characters, each character being between U+20-U+7e.)
        """

        openTypeTagRegex = "[^\u0020-\u007e]"

        if len(string) > 4:
            raise ValueError("Your tag must contain no more than 4 characters.")

        find = re.findall(openTypeTagRegex, string)

        if len(find) > 0:
            raise ValueError(f"The tag contains the following: {', '.join(find)}. This is not valid. It must only contain certain characters. These include alphanumeric characters and some symbols. (In techspeak - only in the unicode range U+20-U+7e.)")

        self.tag = string

    def __str__(self):
        return self.tag

    def __repr__(self):
        return str(self.tag)

    def __int__(self):
        """
        Converts tag to it's data representation in an OpenType font.

        (Array of 4 UInt8s, each UInt8 representing each character's Unicode codepoint.)

        ie.
        "OTTO"
        = 0x4F54544F

        (O  T  T  0 )
        (4F 54 54 4F)
        """

        tagList = list(self.tag)
        intList = [f"{ord(t):2x}" for t in tagList]

        return int(intList[0] + intList[1] + intList[2] + intList[3], 16)



class bFlags:
    """
    Class encapsulating binary flags in font tables.
    """
    def __init__(self, string):
        """
        Binary flags are stored in big-endian order. (ie. left-to-right)
        """

        self.bits = []

        if type(string) is not str:
            raise ValueError("Making binaryFlags data type failed. Input data is not a string.")

        for c in string:
            if c not in ['1', '0', ' ']:
                raise ValueError(f"Making binaryFlags data type failed. The string that was entered contained characters other than '1', '0' or space. You gave '{c}'.")
            if c in ['1', '0']:
                self.bits.append(int(c))




    def toTTXStr(self):
        """
        Returns a string that's little-endian formatted, for TTX use.
        """

        ttxString = ""

        for index, c in enumerate(self.bits[::-1]): # reverse order
            if index%8 == 0 and index != 0: # every 8 bits, add a space.
                ttxString += ' '
            ttxString += str(c) # append the bit as a string
            
        return ttxString


    def toBinary(self):
        """
        returns binary output that's big-endian formatted, for binary compiler use.
        TODO: actually make this work.
        """
        return '0'

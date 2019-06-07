import re
import struct
import sys
from math import floor
from datetime import datetime, tzinfo, timedelta, timezone


class tag:
    """
    Class encapsulating an TrueType/OpenType tag data type.
    - https://docs.microsoft.com/en-us/typography/opentype/spec/otff#data-types
    """

    def __init__(self, string):
        """
        Initialises a tag based on a string.
        Ensures that a string is compliant with OpenType's tag data type.

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
        Converts tag to it's expected representation in an OpenType font.

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

    def toBytes():
        """
        Returns the tag's int representation as bytes in big-endian format.
        """
        return int(self).to_bytes(self.len, 'big')





class bFlags:
    """
    Class encapsulating binary flags in font tables.
    """

    def __init__(self, string):
        """
        Binary flags are entered in big-endian order. (ie. left-to-right).
        Input can be formatted with spaces (ie. '00100000 00001010').
        Binary flags can only be 8, 16 or 32 bits long.
        """

        if type(string) is not str:
            raise ValueError("Making binaryFlags data type failed. Input data is not a string.")

        string = string.translate({ord(' '):None}) # strip spaces

        if len(string) not in [8, 16, 32]:
            raise ValueError(f"Making binaryFlags data type failed. The amount of bits given was not 8, 16 or 32. It has to be one of these.")

        self.len = floor(len(string)/8)

        if sys.byteorder == 'little':
            string = string[::-1] # reverse the byte order if system is little endian.

        try:
            self.bits = int(string, 2)
        except ValueError as e:
            raise ValueError(f"Making binaryFlags data type failed. -> {e}")



    def __str__(self):
        """
        Returns a string-formatted list of bits, with spacing every 8 bits.
        In big-endian byte order (first to last).
        """
        string = ""
        bitString = f"{self.bits:0{self.len*8}b}"

        if sys.byteorder == 'little': # ensure what we're working with is big-endian.
            bitString = bitString[::-1]

        for index, c in enumerate(bitString): # big-endian
            if index%8 == 0 and index != 0: # every 8 bits, add a space.
                string += ' '
            string += str(c) # append the bit as a string

        return string


    def __repr__(self):
        return str(self)


    def set(self, bitNumber, value):
        """
        Sets a bit to a specific binary value.
        """
        self.bits = self.bits & ~(1 << bitNumber) | (value << bitNumber)


    def toTTXStr(self):
        """
        Returns a string that's little-endian formatted, for TTX use.
        """
        return str(self)[::-1] # just get reverse str(), since str() guarantees big-endian.


    def toBytes(self):
        """
        Returns bytes in big-endian format.
        """
        return self.bits.to_bytes(self.len, 'big')







class fixed:
    """
    A representation of a 'Fixed' data type in a font. This is used in normal fixed values, as well as by head.fontRevision.
    (A decimal number where the two numbers on either side of the decimal represent exactly 16 bits.)

    - https://docs.microsoft.com/en-us/typography/opentype/spec/otff#table-version-numbers
    - https://silnrsi.github.io/FDBP/en-US/Versioning.html
    """
    def __init__(self, string):

        versionComponents = string.split('.')

        # normal decimal versions
        self.majorVersionSimple = versionComponents[0]
        self.minorVersionSimple = versionComponents[1]

        try:
            # creating an OpenType-compliant fontRevision number based on best practices.
            # https://silnrsi.github.io/FDBP/en-US/Versioning.html
            self.majorVersionCalc = int(versionComponents[0])
            self.minorVersionCalc = int(( int(versionComponents[1]) / 1000 ) * 65536)
        except:
            raise Exception("Converting headVersion to it's proper data structure failed for some reason!" + str(e))


    def __str__(self):
        """
        Returns a friendly, non-weird version of it.
        """
        return self.majorVersionSimple + '.' + self.minorVersionSimple


    def toHex(self):
        """
        Returns a proper hexidecimal representation of the version number as a string.
        """
        return '0x' + f"{self.majorVersionCalc:04x}" + f"{self.minorVersionCalc:04x}"


    def __int__():
        """
        Returns the proper hexadecimal representation of this value.
        ie.

        1.040
        000010a3d

        1   . 040
        0001  0a3d
        """
        return int(f"{self.majorVersionCalc:04x}" + f"{self.minorVersionCalc:04x}", 16)







class vFixed:
    """
    A specific, non-normal representation of a fixed number, used only in certain forms of version numbers.

    - https://docs.microsoft.com/en-us/typography/opentype/spec/otff#table-version-numbers
    """

    def __init__(self, string):

        versionComponents = string.split('.')

        # normal decimal versions
        self.majorVersion = int(versionComponents[0])
        self.minorVersion = int(versionComponents[1])

    def __int__(self):
        return (f'{self.majorVersion:>04x}' + f"{self.minorVersion:<04d}", 16)

    def toHexStr(self):
        return "0x" + f'{self.majorVersion:>04x}' +  f"{self.minorVersion:<04d}"

    def toDecimalStr(self):
        return str(self.majorVersion) + '.' + str(self.minorVersion)







class longDateTime:
    """
    Class representing the LONGDATETIME data format in fonts.

    LONGDATETIME is an Int64 representing the amount of seconds since 1st January 1904 at 00:00 UTC.
    - https://docs.microsoft.com/en-us/typography/opentype/spec/otff#data-types

    LONGDATETIME is done at UTC; there are no time zones.
    """

    def __init__(self, string=None):
        """
        Either takes in a formatted string representing a datetime, or nothing.
        If nothing is inputted, forc will just use now.

        forc's datetime format:
        (Microseconds assumed to be 0.)

        2019-05-22 09:59 +0000
        %d-%m-%d   %H:%M %z
        """

        if string and string != "":
            try:
                self.datetime = datetime.strptime(string, "%Y-%m-%d %H:%M %z")
            except:
                raise ValueError(f"Creating longDateTime data type failed. The string given ('{string}') is formatted wrong.")
        else:
            self.datetime = datetime.now(timezone.utc)


    def __int__(self):
        """
        Returns an int representation of this datetime, designed for font binary compilation.
        (Returns a time delta in seconds from 1st January 1904 at 00:00 UTC to this datetime at UTC.)
        """
        firstDate = datetime(1904, 1, 1, 0, 0, 0, 0, timezone.utc)
        delta = self.datetime - firstDate

        return floor(delta.total_seconds()) # return a rounded-down integer of the total seconds in that delta.



    def toTTXStr(self):
        """
        Returns a string representation of this datetime, designed for TTX compilation.
        (returns a datetime string formatted in the following way:)

        %a  %b  %d %X       %Y
        Wed May 22 13:45:00 2018
                   (24h UTC)

        (Giving TTX compiler anything else will result in a TTX build error)
        """
        return self.datetime.strftime("%a %b %d %X %Y")

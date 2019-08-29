import sys
import struct
from math import floor

def generateOffsets(list, length, offsetStart, usingClasses=True):
    """
    Takes a list of classes that have a .toBytes() function, and then converts
    it to Bytes with that function and generates a matching list of offsets.

    inputs:
    - array: the array of classes that has a .toBytes() function.
    - length: length of each offset: 32 (4 bytes/UInt32) or 16 (2 bytes/UInt16).
    - offsetStart: the number of bytes you want the offsets to begin at. (normally a negative number)

    Returns an object with the compiled bytes of offsets (["offsets"]), then the compiled blob of bytes (["bytes"]).

    - https://docs.microsoft.com/en-us/typography/opentype/spec/otff#data-types
    """

    # check the input first

    if length not in [16, 32]:
        raise ValueError(f"generateOffsets requires a bit length of either '16' or '32'. You gave '{length}'.")

    if usingClasses:
        for num, x in enumerate(list):
            try:
                temp = x.toBytes()
            except ValueError as e:
                raise ValueError(f"The list given to generateOffsets must be classes that all have a toBytes() function. Item {num} in this list doesn't.")

    if offsetStart < 0:
        raise ValueError(f"The offsetStart given was a negative number ({offsetStart}). It can't be a negative number.")


    # now do the conversion

    offsetBytes = b'' # each offset number as bytes, cumulatively calculated
    bytesBlob = b'' # the entire compacted blob of bytes

    offsetInts = [] # each offset as ints, to temporarily run totals on

    for x in range(0, len(list)):

        # convert this object into bytes, add it to The Blob.
        if usingClasses:
            objectInBytes = list[x].toBytes()
        else:
            objectInBytes = list[x]

        bytesBlob += objectInBytes


        # cumulatively add the offset position for this particular section of The Blob.
        if x == 0:
            offsetInt = offsetStart
        elif x > 0:
            if usingClasses:
                prevBytesLen = len(list[x-1].toBytes())
            else:
                prevBytesLen = len(list[x-1])
            offsetInt = offsetInts[-1] + prevBytesLen

        offsetInts.append(offsetInt)

        # represent the offset position as bytes, ready for output into a neat list
        offset = b''
        if length == 16:
            offset = struct.pack( ">H", offsetInt) # Offset16 (UInt16)
        elif length == 32:
            offset = struct.pack( ">I", offsetInt) # Offset32 (UInt32)

        offsetBytes += offset

    return {"offsetBytes": offsetBytes, "offsetInts": offsetInts, "bytes": bytesBlob}




def calculateTableChecksum(data):
    """
    Calculates checksums for tables.

    If the data length is not a multiple of 4, it assumes it
    should be padded with null bytes to make it so.

    Should not be used on anything but the bytes output of a whole table.

    - https://docs.microsoft.com/en-us/typography/opentype/spec/otff#calculating-checksums
    (code being used from fonttools - https://github.com/fonttools/fonttools/blob/master/Lib/fontTools/ttLib/sfnt.py)
    (I don't have to credit fonttools, I just wanted to~)
    """

    remainder = len(data) % 4

    if remainder:
        data += b"\0" * (4 - remainder)

    value = 0
    blockSize = 4096
    assert blockSize % 4 == 0

    for i in range(0, len(data), blockSize):
        block = data[i:i+blockSize]
        longs = struct.unpack(">%dL" % (len(block) // 4), block)
        value = (value + sum(longs)) & 0xffffffff

    return value



def outputTableBytes(data):
    """
    Outputs table bytes in a specific way that makes them ready to be composed into a font file.

    It returns a tuple containing:
    [0] The bytes output of the table, but padded so it's 32-bit aligned (is a multiple of 4 bytes).
    [1] The length of the unpadded bytes output of the table.

    The original length is necessary for TableRecord entries. (https://docs.microsoft.com/en-us/typography/opentype/spec/otff#calculating-checksums)

    This function should only be used on the output of each table as a whole.

    - https://docs.microsoft.com/en-us/typography/opentype/spec/otff#font-tables
    """
    remainder = len(data) % 4

    if remainder:
        return (data + b"\0" * (4 - remainder), len(data)) # pad with zeroes
    else:
        return (data, len(data))

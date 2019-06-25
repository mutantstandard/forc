import sys
import struct
from math import floor

def generateOffsets(list, length, offsetStart):
    """
    Takes a list of classes that have a .toBytes() function, and then converts
    it to Bytes with that function and generates a matching list of offsets.

    inputs:
    - array: the array of classes that has a .toBytes() function.
    - length: length of each offset: "long" (4 bytes/UInt32) or "short" (2 bytes/UInt16).
    - offsetStart: the number of bytes you want the offsets to begin at. (normally a negative number)

    Returns an object with the compiled bytes of offsets (["offsets"]), then the compiled blob of bytes (["bytes"]).

    - https://docs.microsoft.com/en-us/typography/opentype/spec/otff#data-types
    """

    if length not in [16, 32]:
        raise ValueError(f"generateOffsets requires a bit length of either '16' or '32'. You gave '{length}'.")

    for num, x in enumerate(list):
        try:
            temp = x.toBytes()
        except ValueError as e:
            raise ValueError(f"The list given to generateOffsets must be classes that all have a toBytes() function. Item {num} in this list doesn't.")

    offsetList = [] # used to calculate the offsets cumulatively.
    bytesBlob = bytes()

    for num, x in enumerate(list):
        bytesChunk = x.toBytes()
        bytesBlob += bytesChunk

        # get 0 + offsetStart for first
        # subsequent ones are sizeof(list[n-1]) + sum(glyphDataOffsetsNum) + offsetStart
        if num == 0:
            offsetNum = 0
        elif num > 0:
            offsetNum = sys.getsizeof(x[-1].toBytes()) + sum(offsetList) + offsetStart

        offset = bytes()
        if length == "short":
            offset = struct.pack( ">H", offsetNum) # Offset16 (UInt16)
        elif length == "long":
            offset = struct.pack( ">I", offsetNum) # Offset32 (UInt32)

        offsetList.append(offset)

    return {"offsets": offsetList, "bytes": bytesBlob}




def calculateChecksum(data):
    """
    Calculates a checksum for a given hunk of data.

    If the data length is not a multiple of 4, it assumes it
    should be padded with null bytes to make it so.

    - https://docs.microsoft.com/en-us/typography/opentype/spec/otff#calculating-checksums
    (code being used from fonttools - https://github.com/fonttools/fonttools/blob/master/Lib/fontTools/ttLib/sfnt.py)
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

import sys
import struct


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


    offsetNumList = [] # used to calculate the offsets cumulatively.
    offsetList = bytearray([])
    bytesBlob = bytearray([])

    for x in range(1, len(list)):
        bytes = x.toBytes()
        bytesBlob.append(bytes)

        # get 0 + offsetStart for first
        # subsequent ones are sizeof(list[n-1]) + sum(glyphDataOffsetsNum) + offsetStart
        if x == 0:
            offsetNum = 0
        elif x > 0:
            offsetNum = sys.getsizeof(x[-1].toBytes) + sum(glyphDataOffsetsNum) + offsetStart

        if length == "short":
            offset = struct.pack( ">H", offsetNum) # Offset16 (UInt16)
        elif length == "long":
            offset = struct.pack( ">I", offsetNum) # Offset32 (UInt32)

        offsetNumList.append(offsetNum)
        offsetList.append(offset)

    return {"offsets": offsetList, "bytes": bytesBlob}



def simpleHexName(int):
    """
    returns a hexadecimal number as a string without the '0x' prefix.
    """

    return (hex(int)[2:])



def glyphName(codepointSeq):
    """
    takes in a codepointSeq (list of hexadecimal numbers)
    and returns a string
    """

    return 'u' + '_'.join(map(simpleHexName, codepointSeq))




def codepointSeq(string, delim_codepoint):
    """
    Tries to break down a sequence of strings formatted as
    hexadecimal numbers into a list of ints.

    Creates an exception if it fails.
    """

    codepoints = []

    try:
        codepoints = [int(c, 16) for c in string.split(delim_codepoint)]
    except ValueError as e:
        raise ValueError("Codepoint sequence isn't named correctly. Make sure your codepoint sequence consists only of hexadecimal numbers and are separated by the right delimiter.")

    return codepoints

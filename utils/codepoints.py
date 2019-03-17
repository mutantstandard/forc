



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

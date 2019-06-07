

# Functions that validate codepoint sequences according to specific criteria.
# All of them will return ValueErrors when they fail.

def testZWJSanity(c):
    """
    Function that tests the sanity of ZWJ placement in a codepoint sequence.

    (ie. ZWJs placed at the beginning or end of a sequence, or two ZWJs placed
    next to each other, is considered 'not sane')
    """
    zwj = 0x200d

    if len(c) > 1 and zwj in c:
        if c[0] == zwj or c[-1] == zwj:
            raise ValueError(f"This codepoint sequence has a ZWJ (U+200d) at the beginning and/or the end of it's codepoint seqence (when ignoring VS16/U+fe0f). This is not valid.")

        if any(c[i]== zwj and c[i+1] == zwj for i in range(len(c)-1)):
            raise ValueError(f"This codepoint sequence has two or more ZWJs (U+200d) next to each other (when ignoring VS16/U+fe0f). This is not a valid.")


def testRestrictedCodepoints(codepointSeq):
    """
    Make sure that each codepoint in a codepoint string is within the right ranges.
    Throws an exception when it is not.
    """
    for c in codepointSeq:
        if c < 0x20:
            raise ValueError(f"This codepoint sequence contains a codepoint that is below U+20. You cannot encode glyphs below this number because various typing environments get confused when you do.")

        if c == 0x20:
            raise ValueError(f"This codepoint sequence contains U+20. This is space - you shouldn't be using a glyph for this.")

        if c == 0xa0:
            raise ValueError(f"This codepoint sequence contains U+a0. This is a space character - you shouldn't be using a glyph for this.")

        if c > 0x10FFFF:
            raise ValueError(f"This codepoint sequence contains a codepoint that is above U+10FFFF. The Unicode Standard currently does not support codepoints above this number.")

    if len(codepointSeq) == 1 and codepointSeq[0] == 0xfe0f:
        raise ValueError(f"'fe0f' by itself is just a service codepoint and cannot be be used as an input.")

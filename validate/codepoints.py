
def testZWJSanity(glyph):
    codepointSeq = glyph.codepoints.seq
    zwj = int('200d', 16)

    if codepointSeq[0] == zwj or codepointSeq[-1] == zwj:
        raise ValueError(f"One of your glyphs ('{glyph}') has a ZWJ at the beginning and/or the end of it's codepoint seqence (when ignoring VS16 (U+fe0f). This is not correct.")

    if any(codepointSeq[i]== zwj and codepointSeq[i+1] == zwj for i in range(len(codepointSeq)-1)):
        raise ValueError(f"One of your glyphs ('{glyph}') has two or more ZWJs (U+200d) next to each other (when ignoring VS16 (U+fe0f)). This is not correct.")


def testRestrictedCodepoints(glyph):
    """
    Make sure that each codepoint in a codepoint string is within the right ranges.
    Throws an exception when it is not.
    """
    for c in glyph.codepoints.seq:
        if c < int('20', 16):
            raise Exception(f"The glyph '{glyph}' contains a codepoint that is below U+20. You cannot encode glyphs below this number because various typing environments get confused when you do.")

        if c == int('20', 16):
            raise Exception(f"The glyph '{glyph}' contains U+20. This is space - you shouldn't be using a glyph for this.")

        if c == int('a0', 16):
            raise Exception(f"The glyph '{glyph}' contains U+a0. This is a space character - you shouldn't be using a glyph for this.")

        if c > int('10FFFF', 16):
            raise Exception(f"The glyph '{glyph}' contains a codepoint that is above U+10FFFF. The Unicode Standard currently does not support codepoints above this number.")

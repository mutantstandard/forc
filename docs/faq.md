# forc FAQ

## Why make this?

- There are no multi-format emoji font compilers out there.
- There are no single-format emoji font compilers that support either arbitrary or non-Unicode Standard codepoints.

------

## How does it work?

forc takes the input data and makes what is called a TTX file - which is an XML representation of a font file. This XML file is then passed to `fonttools`' TTX compiler so it can compile it into a font.

TTX was only really intended as an interchange format, but the reason forc uses TTX is because `fonttools` cannot create a font file by itself and the only open source command line tool that can - `fontforge`, doesn't support emoji glyph tables.

In addition, `fonttools` as a library has little to no documentation so it was easier to find out how TTX works and what makes a valid TTX file than it was to learn how to use `fonttools` directly.

Creating an iOS Configuration Profile is exactly the same process, because it is also XML.

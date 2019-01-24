# forc notes

## Why make this?

- There are no multi-format emoji font compilers out there.
- There are no single-format emoji font compilers that support either arbitrary or non-Unicode Standard codepoints.


## How does it work?

forc takes the input data and makes what is called a TTX file - which is an XML representation of a font file. This XML file is then passed to `fonttools`' TTX compiler so it can compile it into a font.

TTX was only really intended as an interchange format, but the reason forc uses TTX is because `fonttools` cannot create a font file by itself and the only open source command line tool that can - `fontforge`, doesn't support emoji glyph tables.

In addition, `fonttools` as a library has little to no documentation so it was easier to find out how TTX works and what makes a valid TTX file than it was to learn how to use `fonttools` directly.

Creating an iOS Configuration Profile is exactly the same process, because it is also XML.

## What are the details on the formats forc can export to?

####svginot

SVG glyphs are encoded in SVG tables encoded alongside other OpenType-compatible data.

####sbix

PNG glyphs are encoded in sbix tables encoded alongside other TrueType-compatible data.

sbix is also compatible with OpenType, but TrueType data is used to maximise compatibility with Apple platforms.

####CBx

PNG glyphs are encoded in CBDT/CBLC tables encoded alongside other OpenType-compatible data.

This is to mimic how Google encodes their emoji fonts.

In forc, the name 'CBDT/CBLC' is simplified to 'CBx' to make it easier to remember.

## What input image formats are supported?

- SVG (for SVGinOT)
- PNG (for sbix and CBx)

forc will not render SVGs to PNGs. You will need to find something else that can provide that for you.

Only a subset of the SVG format is either compatible or has guaranteed compatibility across text renderers and web browsers.

[Microsoft lists out what's not compatible here.](https://docs.microsoft.com/en-gb/typography/opentype/spec/svg#svg-capability-requirements-and-restrictions). Forc will stop compilation with a warning if it finds these.

Aside from this, the `viewBox` attribute also does not work consistently. forc automatically compensates for this by stripping the attribute and enclosing the svg image in a group with a transform.
# Formats

What formats forc can export to:

### SVG-based formats

You need SVG images in your input to make these:

#### SVGinOT

- SVG glyphs encoded as SVG tables
- OpenType ligature data
- .otf extension

### PNG-based formats

You need PNG images in your input to make these.

The strikes for PNG-based formats are inferred from whatever is inside input folder.

#### sbixTT

- PNG glyphs encoded as sbix tables
- TrueType ligature data
- .ttf extension

macOS's emoji system font format.

#### sbixOT

- PNG glyphs encoded as sbix tables
- OpenType ligature data
- .otf extension

#### sbixTTiOS

sbixTT packaged in an iOS Configuration Profile. Designed for installation in iOS.

#### sbixOTiOS

sbixOT packaged in an iOS Configuration Profile.

This is just a development/research thing and will probably be removed in the first proper release.

#### CBx

- PNG glyphs encoded as CBDT/CBLC tables
- OpenType ligature data
- .ttf extension

This is specifically designed to mimic how Google encodes their emoji fonts.

'CBDT/CBLC' is more commonly used to refer to this format, but in forc it's simplified to 'CBx' to make it easier to remember.


# Formats

There are multiple formats for emoji fonts, and not all of them work in the same way or be accepted by every operating system or device.

These are the formats you'll be able to compile your fonts into.

---

### SVG-based formats

You need SVG images in your input to make these:

#### SVGinOT

Windows 10, macOS 10.14+, Linux, Firefox

*This is a pretty inconsistent format and is currently not recommended for general use.*

- SVG glyphs encoded as SVG tables
- OpenType ligature data
- .otf extension

---

### PNG-based formats

You need PNG images in your input to make these.

The strikes for PNG-based formats are inferred from whatever is inside input folder.


#### sbixOT

Windows 10, macOS 10.7+, Linux

- PNG glyphs encoded as sbix tables
- OpenType ligature data
- .otf extension


#### sbixOTiOS

iOS 7+

sbixOT packaged in an iOS Configuration Profile. If you want your font to be installable on iOS, you need to build this.

You **don't** need to be using macOS to build one of these.


#### CBx

Windows 10, Linux, Rooted Android devices

- PNG glyphs encoded as CBDT/CBLC tables
- OpenType ligature data
- .ttf extension

This is specifically designed to mimic how Google encodes their emoji fonts.

'CBDT/CBLC' is more commonly used to refer to this format, but in forc it's simplified to 'CBx' to make it easier to remember.

---

### Formats that are there but don't work

These are currently placeholders in the software and may be removed in the future, do not use these.

#### sbixTT

- PNG glyphs encoded as sbix tables
- TrueType ligature data
- .ttf extension

macOS's emoji system font format.

#### sbixTTiOS

sbixTT packaged in an iOS Configuration Profile. Designed for installation in iOS.

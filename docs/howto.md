# how to use forc

## Input directory path

### Folder structure

- Needs to contain subfolders representing the formats and/or raster strikes.
- These subfolders need to contain the images in a flat structure.
- The codepoints of images in these subfolders must be identical between each other.
- PNG folder(s) should be in the format `png-<strike size>`, 'strike size' being the resolution of the emoji on a low-DPI screen.
- they should all be lowercase.

```
in
|- svg
|	|-[images]
|
|- png-32
|	|-[images]
|
|- png-64
|	|-[images]
|
|- png-128
	|-[images]

```

### Image formats

forc accepts the following formats:

- SVG (for SVGinOT)
- PNG (for sbix-based formats and CBx)

forc will not render SVGs to PNGs. You will need to find something else that can provide that for you.

forc will only take what it needs, so if you have an input folder with PNGs and SVGs and you're only exporting SVGinOT, forc will only check and use the SVG images and not the others.

### SVG images

When using SVG images, you have to be careful about your contents.

Only a subset of the SVG format is either compatible or has guaranteed compatibility across text renderers and web browsers.

[Microsoft lists out what's not compatible here.](https://docs.microsoft.com/en-gb/typography/opentype/spec/svg#svg-capability-requirements-and-restrictions) Forc will stop compilation with a warning if it finds most of these.

Aside from this, the `viewBox` attribute also does not work consistently. forc automatically compensates for this by stripping the attribute and enclosing the svg image in a group with a transform.

---

## Output directory

All forc exports will be exported in a flat manner, each file named after their respective format.

---


## Manifest
The manifest is a JSON file with a particular structure, and it contains metrics, encoding information and human-readable metadata for the `name` table.

I'll write more about this soon!


---

## Formats

### SVG-based formats

#### SVGinOT

- SVG glyphs encoded as SVG tables
- OpenType ligature data
- .otf extension

### PNG-based formats

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

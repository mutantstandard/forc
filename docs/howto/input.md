# Input

## Folder structure

Your input folder needs to meet the following criteria to be considered valid in orxporter:

- Needs to contain subfolders representing the formats and/or raster strikes.
- These subfolders need to contain the images in a flat structure.
- The codepoints of images in these subfolders must be identical between each other.
- PNG folder(s) should be in the format `png-<strike size>`, 'strike size' being the resolution of the emoji on a low-DPI screen.
- The folder names should all be lowercase.


eg:

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

If you are exporting using [orxporter](https://github.com/mutantstandard/orxporter), using the `-f %f/%u` build flag will guarantee that you make an export that fulfills all of these requirements.

---

## Image formats

forc accepts the following formats:

- SVG (for SVGinOT)
- PNG (for sbix-based formats and CBx)

forc will not render SVGs to PNGs. You will need to find something else that can provide that for you.

forc will only take what it needs, so if you have an input folder with PNGs and SVGs and you're only exporting SVGinOT, forc will only check and use the SVG images and not the others.

### SVG images

When using SVG images, you have to be careful about your contents.

Only a subset of the SVG format is either compatible or has guaranteed compatibility across text renderers and web browsers as part of an SVGinOT font. [Microsoft lists out what's not compatible here](https://docs.microsoft.com/en-gb/typography/opentype/spec/svg#svg-capability-requirements-and-restrictions).

Forc will stop compilation with a warning if it finds most of the aspects of an SVG that are either incompatible or guaranteed not to be compatible.

You can also control how strict you want the checking to be with the `-nusc` build flag. This build flag disables checks for SVG aspects that are not guaranteed to work but are not outright disallowed.

#### Undetected SVG aspects

There are some potentially incompatible aspects of SVGs that forc can't detect:

##### Incompatible
(These will not work.)

- Relative measurements (em, ex, etc.)
- RGBA colours
- CSS2 colour values in styles

##### Unenforced
(These are not guaranteed to work.)

- XML entities

#### SVG aspects that are unreliable

Aside from what's in the OpenType spec, there are some SVG aspects that are not mentioned by the standard that don't work as expected.

- `viewBox` attribute (is incredibly inconsistent and uselesss)
	- forc automatically compensates for this by stripping the attribute and enclosing the svg image in a group with a transform.

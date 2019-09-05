# How to make a font

**Keep in mind that forc is under heavy development and font output isn't fully working yet. This guide is largely written as if font output is basically fine.**

---

There are a few different ingredients you'll need to make a font.

(Many of these flags will be familiar to you if you already use [orxporter](https://github.com/mutantstandard/orxporter).)

### [Input](input.md) `(-i)`

The folder forc uses to find images for glyphs.

### Output `(-o)`

The folder forc outputs to.

All forc exports will be exported in a flat manner, each file named after the filenames you set in the [manifest](manifest.md), or just named after their font format if it's not set.


### [Manifest](manifest.md) `(-m)`

Where you set your font's metrics and metadata.


### [Aliases](aliases.md) `(-a)` (optional)

For when you want to map multiple codepoint sequences onto the same glyph.


### [Formats](formats.md) `(-F)`

What emoji font formats to export to.


### Compiler `(-C)` (optional)

What compiler to use.

This is optional - the default at the moment is `ttx`.

- `ttx` (default): Compiles a TTX representation of the font to hand over to `ttx`/`fonttools`. Some of your values will be overridden by the compiler, and often doesn't work as expected.

- `forc` : forc's built-in binary compiler intended to replace ttx. Currently not working and under development.

---


### Other build flags

All of these are optional.

#### `--ttx`

Exports a ttx version of the font file for each format in their compiled state.

(ie. After compiling the font file, forc runs the file back through `fonttools` to make a TTX.)


#### `--dev-ttx`

Keeps the initial ttx that forc compiles for each format before passing it to `fonttools`.

This is slightly different to `--ttx`, which is a full representation of the font file in it's compiled state.

Mainly useful for forc development, but you also might want to use this option to look deeper at what forc is doing.


#### `--no-vs16`

Strips any presence of VS16 (U+fe0f) that are in the input images from the font output.

VS16 can be pretty annoying and various emoji vendors outright ignore it. This is a simple way to purge that codepoint from your output.


#### `--nusc` (No Unenforced SVG Contents Checking.)

When loading SVG images, forc checks their contents to make sure they are compatible with the SVGinOT standard, and to help you make the most compatible fonts, forc is pretty strict about it by default.

There are different degrees to which a part of an SVG file is compatible with the SVGinOT standard however.

This build flag relaxes the checking a bit, only throwing errors when forc finds something that definitely cannot be in an SVGinOT file.

Only use this if you don't care about compatibility that much and you know what you're doing.


#### `--afsc` (Affinity SVG Correction)

The SVGs exported by the Affinity suite of software by Serif have quirks that clash with being embedded in an SVGinOT font.

It's not that the font won't compile, but the way Affinity colours SVG exports is in such a way that certain shapes have no fill or stroke at all.

For an image, this is fine (it shows as black, which is what it's intended to be), but in a font it means that area will be coloured by whatever the text colour is when in use.

Using this flag will apply corrections to the SVG when they are loaded into forc so this doesn't happen.

**You should always use this if you are inputting SVGs that are coming from Affinity software.**

---


## Limitations

#### Square glyphs only

forc produces monospaced fonts with a square aspect ratio only.

#### Colour glyphs only

forc expects that you only want to compile and see colour emoji data.

Black and white fallback glyphs in `glyf`/`CFF`-style data will not be produced. forc just inserts dummy and empty `glyf` data to please font validation processes.

If a text rendering environment doesn't support colour glyphs, the font will be invisible.

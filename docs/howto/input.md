# Input

## Filenames

Every image file needs to have the name of one or more Unicode codepoints, separated by a delimiter.

- The codepoints have to be hex, without any U+ or 0x at the beginning.
- The delimiter is '-' by default, but you can change it to something else with the `-d` build flag.

The delimiter does not represent a ZWJ, it's just to separate codepoints in a sequence.

Variation selectors (ie VS16/U+fe0f), ZWJ (U+200d) and so on have to be put into the sequence of your filename manually.

eg:

```
(200d = ZWJ)
(fe0f = VS16)

1f3a5.png
1f5ef-fe0f.png
1f446-fe0f-101650-101604.png
1f3f3-200d-1f308.png 

```

If you are using [aliases](aliases.md), your naming convention for those will be exactly the same as what is outlined here.

----

## Folder structure

Your input folder needs to be structured this way:

- Has to contain subfolderes named by format/resolution.
- Each of these subfolders needs to contain all of your images in a flat list.
- PNG subfolders should be in the format `png-<strike size>` (I'll talk about strike size more in a sec).
- All folder names should be lowercase.

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

You don't have to have multiple formats, but only certain image types can be compiled into certain font formats.

Every subfolder has to have the exact same amount of images, each with the same set of filenames. So if you have a picture called '1f3a5' in one of the folders, there has to be an equivalent image with the same name in all of your input folders. If forc finds inconsistencies between the filenames in the subfolders it's using in a build task, it will stop and throw an error.

'Strike size' refers to the size of your PNG images. If you have a folder of 128px emoji, then your strike size is '128', if it's 64px, then the strike size is '64', and so on.


#### Working with orxporter

If you are exporting using [orxporter](https://github.com/mutantstandard/orxporter), using the `-f %f/%u` build flag will guarantee that you make filenames and a folder structure that fulfills all of these requirements.

---

## Image formats

forc accepts the following formats:

- SVG (for SVGinOT)
- PNG (for sbix-based formats and CBx)

forc will not render SVGs to PNGs. You will need to find something else that can provide that for you.

forc will only take what it needs, so if you have an input folder with PNGs and SVGs and you're only exporting SVGinOT, forc will only check and use the SVG images and not the others.

---

## SVG images

When using SVG images, you have to be careful about your contents.

Only a subset of the SVG format is either compatible or has guaranteed compatibility across text renderers and web browsers as part of an SVGinOT font. [Microsoft lists out what's not compatible here](https://docs.microsoft.com/en-gb/typography/opentype/spec/svg#svg-capability-requirements-and-restrictions).

Forc will stop compilation with a warning if it finds most of the aspects of an SVG that are either incompatible or guaranteed not to be compatible.

You can also control how strict you want the checking to be with the `-nusc` build flag. This build flag disables checks for SVG aspects that are not guaranteed to work but are not outright disallowed.

#### Bad parts of SVGs that don't get detected

There are some potentially incompatible aspects of SVGs that forc can't detect:

##### Incompatible parts
(These will not work.)

- Relative measurements (em, ex, etc.)
- RGBA colours
- CSS2 colour values in styles

##### Unenforced parts
(These are not guaranteed to work.)

- XML entities

#### SVG aspects that are unreliable

Aside from what's in the OpenType spec, there are some SVG aspects that are not mentioned by the standard that don't work as expected. The `viewBox` attribute being one of them. 

`viewBox` is incredibly inconsistent and uselesss across vendors, so forc automatically compensates for this by stripping the attribute and enclosing the svg image in a group with a transform.

Keep in mind that because forc applies a transform, this means that the font will only work in horizontal writing orientation, and it will have bad metrics in vertical orientation. This is because the transform will be applied uniformly across both horizontal and vertical coordinate systems, which clash.

This approach might change in the future, but if you want the best shot at making SVGs, make sure your SVG imports don't have a `viewBox` attribute in the first place.

There may also be other unforseen issues because SVGinOT is generally a very unpredictable format.
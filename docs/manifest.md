# Manifest
The manifest is a JSON file with a particular structure, and it contains metrics, encoding information and human-readable metadata for your font.

This has been structured in such a way where data points that recur throughout a font file have been consolidated in one place.

There are three main sections to the file:

- Metrics
- Encoding
- Metadata

```

{ "metrics" : {...}
, "encoding" : {...}
, "metadata" : {...}
}
```

----

## Metrics

````

{"metrics":
    {"xMin": 0
    ,"xMax": 2048
    ,"yMin": -470
    ,"yMax": 1578
    ,"width": 2048
    ,"height": 2048
    ,"OS2WeirdDescent": 0
	...etc
    }
````


All of these entries shown below are required.

If you don't have a clear idea what you should set yours to, you should set them to the recommended values below. These recommended values are based on metrics found in other emoji fonts, so they will have the best compatibility.

FUnits stands for Font Design Units.

| name | type | rec. value | description |
|:--|:--|--:|:--|
| unitsPerEm | int (FUnits) | 2048 | How many FUnits are in the Em Square. Essentially this means how many arbitrary units of precision are there within your emoji square. This value is the basis for every other value in this section that's based on FUnits. |
| lowestRecPPEM | int (pixels) | | The smallest readable size of your font. |
| width | int (FUnits) | 2048 | Absolute width of your glyphs. |
| height | int (FUnits) | 2048 | Absolute height of your glyphs.  |
| xMin | int (FUnits) |  | The minimum x-position of your glyphs (includes vertical descenders). |
| xMin | int (FUnits) |  | The maximum x-position of your glyphs (includes vertical ascender). |
| yMin | int (FUnits) | | The minimum y-position of your glyphs (includes horizontal descenders). |
| yMax | int (FUnits) | | The maximum y-position of your glyphs (includes vertical ascenders). |
| spaceHLength | int (FUnits) | | The length of space characters in horizontal writing orientation. |
| spaceVLength | int (FUnits) | | The length of space characters in vertical writing orientation. |
| normalWidth | int (FUnits) | | ??? |
| normalLSB | int (FUnits) | | ??? |
| normalHeight | int (FUnits) | | ??? |
| normalTSB | int (FUnits) | | ??? |
| OS2ySubscriptXSize | int (FUnits) | | X-size of glyphs when in subscript. |
| OS2ySubscriptYSize | int (FUnits) | | Y-size of glyphs when in subscript. |
| OS2ySubscriptXOffset | int (FUnits) | | X-offset of glyphs when in subscript. |
| OS2ySubscriptYOffset | int (FUnits) | | Y-offset of glyphs when in subscript. |
| OS2ySuperscriptXSize | int (FUnits) | | X-size of glyphs when in superscript. |
| OS2ySuperscriptYSize | int (FUnits) | | Y-size of glyphs when in superscript. |
| OS2ySuperscriptXOffset | int (FUnits) | | X-offset of glyphs when in superscript. |
| OS2ySuperscriptYOffset | int (FUnits) | | Y-offset of glyphs when in superscript. |
| OS2yStrikeoutSize | int (FUnits) | | The thickness of the strikeout stroke. |
| OS2yStrikeoutPosition | int (FUnits) | | The distance between the baseline and the top of the strikeout stroke. |


forc is currently only capable of generating monospace fonts with square proportions; you can't set different metrics for specific characters.

forc assumes you want to create a font that can work in both vertical AND horizontal writing orientations. You cannot make a font that only works for one writing orientation.

---

## Encoding

````
,"metadata":
	{ "macLangID": "0"
	, "msftLangID": "0x809"
	}
````

| name | type | req? | description |
|:--|:--|:--|:--|
| macLangID | string representing a number | ✔️ | [Macintosh Language ID](https://docs.microsoft.com/en-us/typography/opentype/spec/name#platform-specific-encoding-and-language-ids-macintosh-platform-platform-id--1). If in doubt, set it to 0 (Roman).
| msftLangID | string representing a hexadecimal number | ✔️ | [Windows Language ID](https://docs.microsoft.com/en-us/typography/opentype/spec/name#windows-language-ids). If in doubt, set it to 0x0409 (American English).




----

## Metadata

````
,"metadata":
	{"created": "Mon Jan 03 13:45:00 2019"
    ,"version": "1.040"
    ,"OS2VendorID": "MTNT"
    ,"nameRecords": {...}
	}
````

| name | type | req? | description |
|:--|:--|:--|:--|
| created | string | ✔️
| version | string (representing a 3-decimal number that's 1.000 or greater) | ✔️
| OS2VendorID | string (a 4-character string of a limited set of ASCII characters) | | [Microsoft's 4-letter identifier for registered font vendors](https://docs.microsoft.com/en-us/typography/opentype/spec/os2#achvendid). |
| nameRecords | object | ✔️ | A structure represnting all of the records of the `name` table. (Described in more detail later.) |


### Name Records

Name records consists of a series of objects named after the font formats that forc can export (or 'default'), 

````
,"nameRecords":
        {"default":
            {"0" : "Copyright (c) 2017-2019 Dzuk (https://noct.zone)"
            ,"2" : "Regular"
            ,"5" : "(0.4.0 - 2019-03-15)"
            ,"8" : "Mutant Standard"
            ,"9" : "Dzuk"
            ,"10" : "The special emoji in this font have important limitations you should understand before using it. See [URL] for more information."
            ,"11" : "https://mutant.tech"
            ,"12" : "https://noct.zone"
            ,"13" : "Mutant Standard emoji is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License."
            ,"14" : "https://creativecommons.org/licenses/by-nc-sa/4.0/"
            ,"16" : "Mutant Standard emoji"
            }
        ,"SVGinOT":
            {"1" : "Mutant Standard emoji (SVGinOT)"
            ,"3" : "Mutant Standard emoji SVGinOT"
            ,"4" : "Mutant Standard emoji (SVGinOT) 0.4.0"
            ,"6" : "MutantStandard-SVGinOT"
            ,"17" : "SVGinOT"
            }
          ...etc.
         }
````

The records in `default` are the values forc will use if there are no values set for the specific format. This way you can repeat name records across formats while also making exceptions.

In order to make a valid manifest, forc doesn't dictate that you must have any one particular sub-object in name records (ie. for SVGinOT format, you can use 'default', 'SVGinOT' or both), just so long as the result is a complete minimum set of name records for every format you're exporting to.

Inside each set are more objects. Name-value pairs of numbers (formatted as strings) paired with the name record corresponding to that number.

#### All of the name records

All name records need to be formatted as strings.

Descriptions that are in bold are the most significant/important things.

What kinds of characters you can put in these will be determined by the encoding IDs you've set in the encoding section (as described earlier in this document).

| num. | req? | description | example | notes |
|:--:|:---:|:--|:---|:---|
| 0 |   | **Copyright** | Copyright © 2017-2019 Dzuk (https://noct.zone) | Identifies the copyright holder of the font. This isn't where the license goes - use name records 13 and 14 for license information. This isn't necessarily the same as the designer (name record 9) or the vendor (name record 8). |
| 1 | ✔️ | **Family** | Mutant Standard emoji (SVGinOT) | [3]
| 2 | ✔️ | **Subfamily** | Regular | [3]
| 3 | ✔️  | **Unique font identifier** | Mutant Standard emoji SVGinOT | It's a string that distinguishes your font from others. Include version information here. macOS will consider the structure of this table invalid if this is not present. | 
| 4 | ✔️ | **Full font name** | Mutant Standard emoji (SVGinOT) | A combination of 1 + 2, or 16 + 17.
| 5 | | **Version supplementary information** | (0.4.0 - 2019-03-15) | **This is a special case that doesn't fully represent what this field normally is.** [4] |
| 6 | ✔️ | **PostScript name** | MutantStandard-SVGinOT | Has to be restricted to 'printable' ASCII characters. (U+0021 through U+007E, and not '[', ']', '(', ')', '{', '}', '<', '>', '/', and '%'.)|
| 7 |   | Trademark |  |
| 8 |   | **Manufacturer name** | Mutant Standard | Who publised the font. |
| 9 |   | **Designer name** | Dzuk | Who designed the font.
| 10 |   | Description | When using the special emoji within this font that aren't supported by Unicode, make sure you are not using them in situations where other people or devices may not have this font installed, or those who are visually impaired. See [URL] for more information. | 
| 11 |   | **Vendor URL** | https://mutant.tech | [1]
| 12 |   | **Designer URL** | https://noct.zone | [1]
| 13 |   | **License** | Mutant Standard emoji is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. | [2]
| 14 |   | **License URL** | https://creativecommons.org/licenses/by-nc-sa/4.0/ |  [1][2]
| 15 |   | | |
| 16 | ✔️ | **Typographic/Preferred Family** | Mutant Standard emoji | [3]
| 17 | ✔️ | **Typographic/Preferred Subfamily** | SVGinOT | [3]
| 18 |   | Compatible Full |  | 
| 19 |   | Sample Text |  | Sample text for your font. The encoding you choose above limits what characters you can put in here, so you may have limited or no ability to create emoji sample text.
| 20 |   | PostScript CID findfont name | | 
| 21 |   | WWS Family Name | | 
| 22 |   | WWS Subfamily name | | 
| 23 |   | Light Background Palette | | 
| 24 |   | Dark Background Palette | | 
| 25 |   | Variations PostScript Name Prefix | | 

1. URLs have to contain the protocol (ie. http://, ftp://, mailto:).
2. 'License' should just have a brief summary of the license, not legalese. Use 'License URL' to direct people to the legalese.
3. 1 and 2 are similar to 16 and 17 but not identical. 1 and 2 are legacy versions and are strictly restricted to 'Regular', 'Italic', 'Bold' and 'Bold Italic'. With 16 and 17 you can put whatever you want in them. If an application supports 16 and 17, they will take precedence over 1 and 2. If it doesn't, it will just use 1 and 2.
4. This normally a mandatory record but forc uses the version number already recorded in `metadata.version` to create the version record. So in forc, this is just a space for any supplementary information you want to insert after the version number. If you don't want to add any notes, you don't have to, forc will create this record anyway.
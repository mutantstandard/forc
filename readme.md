# forc

Forc (a terrible portmanteau of font and orc) is a font compiler, leveraging fonttools' TTX compiler (by proxy, by creating a TTX file that's then fed to it instead of directly using fonttools) to create valid custom emoji fonts that are compatible with a wide variety of platforms.

This is currently just a prototype to speed up the font prototyping process for Mutant Standard's fonts.

Eventually, either this (or bits of this code) will form the basis of an actual font compiler that can be used with orxporter.

## Planned Features

**Exports to:**

- SVGinOT (Linux, Windows 10, Firefox 50+, macOS 10.14+)
- sbix (macOS 10.7+)
- sbix packaged in a iOS Configuration Profile (iOS 7+)
- CBx (Certain Samsung phones, rooted Android devices)


**Other features:**

- Arbitrary Unicode codepoints - you can use whatever codepoints you want, including PUA.
- Support for ligatures
- Support for VS16


## Limitations


### Current

I'm still learning how to encode fonts, so these will quickly clear up as time goes on.

- Currently only SVGinOT and sbix formats have been tested working.
- Currently all of the formats are only considered valid and work in macOS 10.14 and iOS 12.
- Metrics between SVGinOT and sbix are not consistent.
- I can't get consistent or usable metrics in vertical writing orientation.
- Ligatures don't work yet
- VS16 support has not yet been implemented.


### Planned

- You can't have black and white fallbacks. forc just inserts dummy and empty `glyf` data to please font validation processes. forc expects that you only want to compile and see colour emoji data.


## Dependencies

- `fonttools` (eventually, not actually being used just yet)

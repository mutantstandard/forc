# forc

Forc (a terrible portmanteau of font and orc) is an emoji font compiler, taking in folders of codepoint-named images and a manifest file and returning font files that are compatible with a variety of platforms.

This can either be used by itself or (eventually) from orxporter as part of an emoji build.

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
- Can be used from orxporter for seamlessly building an entire set of emoji.


## Limitations


### Current

I'm still learning how to encode fonts, so these will quickly clear up as time goes on.

- Currently only sbix output has been tested working.
- Currently all of the formats are only considered valid in macOS 10.14 and iOS 12.
- Metrics are not consistent across formats.
- I can't get consistent or usable metrics in vertical writing orientation.
- Ligatures aren't supported yet.
- VS16 support has not yet been implemented.
- Currently doesn't have the code supporting iOS Configuration Profile output.


### Planned

- You can't have black and white fallbacks. forc just inserts dummy and empty `glyf` data to please font validation processes. forc expects that you only want to compile and see colour emoji data.


## Dependencies

- `lxml`
- `fonttools`

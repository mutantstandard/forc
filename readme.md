# forc

Forc (a terrible portmanteau of font and orc) is an emoji font compiler, taking in folders of codepoint-named images and a manifest file and returning fonts that are compatible with a variety of platforms.

This can either be used by itself or (eventually) from orxporter as part of an emoji build.

## Disclaimer

This is an insider tool that has been open sourced, but feature requests and collaboration are welcome to make it more useful for other people. Any collaborators must follow [Mutant Standard's code of conduct](code_of_conduct.md).

## Features

**Exports to:**

- SVGinOT (Linux, Windows 10, Firefox 50+, macOS 10.14+)
- sbix (macOS 10.7+)
- sbix packaged in a iOS Configuration Profile (iOS 7+)
- CBx (Certain Samsung phones, rooted Android devices)


**Other features:**

- Arbitrary Unicode codepoints - you can use whatever codepoints you want, including PUA.
- Support for ligatures.
- Support for VS16.
- Can be used from [orxporter](https://github.com/mutantstandard/orxporter) for seamlessly building an entire set of emoji.


## Limitations

forc is still in development and is not ready for use:

### Current

I'm still learning how to encode fonts, so these will quickly clear up as time goes on.

- Currently only sbix and SVGinOT fonts are visible and working.
- Currently all of the formats generated are only considered valid in macOS 10.14 and iOS 12.
- Metrics are not consistent across formats.
- I can't get consistent or usable metrics in vertical writing orientation.
- VS16 support isn't 100%
- It currently doesn't have the code supporting iOS Configuration Profile output.
- There's no documentation on how to make manifests yet.


### Planned

- You can't have black and white fallbacks. forc just inserts dummy and empty `glyf` data to please font validation processes. forc expects that you only want to compile and see colour emoji data.


## Dependencies

- Python 3.6+
- [lxml](https://lxml.de/)
- [fonttools](https://github.com/fonttools/fonttools)


## License

forc is licensed under [AGPL 3.0](license.txt).

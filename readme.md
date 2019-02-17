# forc

Forc (a terrible portmanteau of font and orc) is an emoji font compiler, taking in folders of codepoint-named images and a manifest file and returning fonts that are compatible with a variety of platforms.

This can either be used by itself or (eventually) from orxporter as part of an emoji build.

## Disclaimer

This is an insider tool that has been open sourced, but feature requests and collaboration are welcome to make it more useful for other people. Any collaborators must follow [Mutant Standard's code of conduct](code_of_conduct.md).

## Features

**Exports to:**

- **SVGinOT**: SVGinOT
- **sbixTT**: (macOS format) sbix with TrueType ligatures 
- **sbixOT**: sbix with OpenType ligatures
- **sbixTT for iOS**: (iOS format) sbix with TrueType ligatures, packaged in an iOS Configuration Profile.
- **sbixOT for iOS**: sbix with OpenType ligatures, packaged in an iOS Configuration Profile. (currently just a development/research thing)
- **CBDT/CBLC** (Google/Android format)


**Other features:**

- Arbitrary Unicode codepoints - you can use whatever codepoints you want, including PUA.
- Support for ligatures.
- Support for VS16.
- Support for ZWJ.
- Can be used from [orxporter](https://github.com/mutantstandard/orxporter) for seamlessly building an entire set of emoji.
- Strict validation of codepoints and metadata, making sure you make valid and highly compatible fonts.


## Limitations

forc is still in development and is not ready for use. Various exports will only either work in limited contexts, with certain kinds of inputs or will not be complete, valid fonts.


## Planned Limitations

Black and white fallbacks will not be produced. forc just inserts dummy and empty `glyf` data to please font validation processes. forc expects that you only want to compile and see colour emoji data. forc font exports can only be seen in computing environments that support colour glyphs.


## Dependencies

- Python 3.6+
- [lxml](https://lxml.de/)
- [fonttools](https://github.com/fonttools/fonttools)

## Collaborators
- Dzuk
- kiilas (thanks for all the help!)

## License

forc is licensed under [AGPL 3.0](license.txt).

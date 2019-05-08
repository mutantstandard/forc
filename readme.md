# forc

![forc logo with the text 'forc' next to it on a blue background](docs/img/forc_logo.png)

Forc (a terrible portmanteau of font and orc) is an emoji font creation tool. It takes in folders of codepoint-named images and a manifest file and returns highly-compatible emoji fonts that can work in a wide variety of platforms.


## Disclaimer

This is an insider tool that has been open sourced, some effort has been made to make it friendly to use for other people, but maybe not enough.

Feature requests and collaboration are welcome. Any collaborators must follow [Mutant Standard's code of conduct](code_of_conduct.md).

## Features

**Exports to:**

- **SVGinOT**: SVGinOT
- **sbixOT**: sbix with OpenType ligatures
- **sbixOT for iOS**: sbix with OpenType ligatures, packaged in an iOS Configuration Profile.

**In development/experimental export options:**

- **CBDT/CBLC** (Google/Android format)
- **sbixTT**: sbix with TrueType ligatures (macOS format)
- **sbixTT for iOS** sbix with TrueType ligatures, packaged in an iOS Configuration profile. (iOS format)


**Other features:**

- Full range of unicode codepoints supported, including the SPUA planes.
- Support for ligatures.
- Support for VS16 (U+FE0F) handling.
- Support for ZWJ (U+200D) handling.
- Many-to-one codepoint sequence to glyph relationships via Alias Glyphs.
- Strictly validates your input and gives you helpful error messages, ensuring that you get it right every time.


## Limitations

forc is still in development and is not ready for use. Various exports will only either work in limited contexts, with certain kinds of inputs or will not be complete, valid fonts.


## Dependencies

- Python 3.6+
- [lxml](https://lxml.de/)
- [fonttools](https://github.com/fonttools/fonttools)

## Collaborators
- Dzuk
- kiilas (thanks for all the help!)

## License

- forc is licensed under [AGPL 3.0](license.txt).
- The forc logo image is ©2019 Dzuk.

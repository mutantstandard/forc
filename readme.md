# forc

![forc logo with the text 'forc' next to it on a blue background](docs/img/forc_logo.png)

forc (a terrible portmanteau of font and orc) is an emoji font creation tool. It takes in folders of codepoint-named images and a manifest file and returns highly-compatible emoji fonts that can work in a wide variety of platforms.

Making fonts can be really hard, so forc is designed to help you succeed every time - it has comprehensive documentation and guides on how to make your own emoji font, gives very readable and transparent error messages and is structured in a way that tries to make making highly-compatible emoji fonts as effortless as possible.

Because fonts are inconsistent and difficult, forc also tries to have a heavily documented and commented codebase, so all of the elements make as much sense as possible to someone new to TrueType/OpenType.

**Forc is under heavy development right now. Most font exports don't work quite right or are not functional yet.**

## Features

**Exports to:**

- **SVGinOT**: SVGinOT
- **sbixOT**: sbix with OpenType ligatures
- **sbixOT for iOS**: sbix with OpenType ligatures, packaged in an iOS Configuration Profile.
- **sbixTT**: sbix with TrueType ligatures
- **sbixTT for iOS** sbix with TrueType ligatures, packaged in an iOS Configuration profile.
- **CBDT/CBLC** (Google/Android format)

**Other features:**

- Full range of unicode codepoints supported, including the SPUA planes.
- Support for ligatures.
- Support for VS16 (U+FE0F) handling.
- Support for ZWJ (U+200D) handling.
- Many-to-one codepoint sequence to glyph relationships via Alias Glyphs.
- Strictly validates your input and gives you helpful error messages, ensuring that you get it right every time.
- Designed to work as effortlessly as possible with [orxporter](https://github.com/mutantstandard/orxporter).

## Dependencies

- Python 3.6+
- [lxml](https://lxml.de/) (install via pip)
- [fonttools](https://github.com/fonttools/fonttools) (install via pip)


## Documentation

#### [How to make a font](docs/howto/howto.md)

#### [FAQ](docs/faq.md)

## Collaborators
- Dzuk
- kiilas

## Contributions

Feature requests and collaboration are welcome. Any collaborators must follow [Mutant Standard's code of conduct](code_of_conduct.md).

## License

- forc is licensed under [AGPL 3.0](license.txt).
- The forc logo image is ©2019 Dzuk.


**Due to [changing project priorities](https://blog.mutant.tech/index.php/2022/12/14/future-priorities/), I have decided to officially shelve this software as of December 2022. Feel free to fork it and keep on working on it if you like, but it doesnt make sense for me to work on it any longer <3**

----

# forc

![forc logo with the text 'forc' next to it on a blue background](docs/img/forc_logo.png)

forc (a terrible portmanteau of font and orc) is an emoji font creation tool. It takes in folders of codepoint-named images and a manifest file and returns highly-compatible emoji fonts that can work in a wide variety of platforms.

Making fonts can be really hard, so forc is designed to help you succeed every time - it has comprehensive documentation and guides on how to make your own emoji font, gives very readable and transparent error messages and is structured in a way that tries to make making highly-compatible emoji fonts as effortless as possible.

Because fonts are inconsistent and difficult, forc also tries to have a heavily documented and commented codebase, so all of the elements make as much sense as possible to someone new to TrueType/OpenType.

---

## Features

**Exports to:**

- **SVGinOT**
- **sbixOT**: sbix with OpenType ligatures.
- **sbixOT for iOS**: sbix with OpenType ligatures, packaged in an iOS Configuration Profile.
- **CBx (CBDT/CBLC)**: CBDT/CBLC tables with OpenType ligatures.

**Other features:**

- Full range of unicode codepoints supported, including the SPUA planes.
- Support for ligatures.
- Support for VS16 (U+FE0F) handling.
- Support for ZWJ (U+200D) handling.
- Many-to-one codepoint sequence to glyph relationships via Alias Glyphs.
- Strictly validates your input and gives you helpful error messages, ensuring that you get it right every time.
- Designed to work as effortlessly as possible with [orxporter](https://github.com/mutantstandard/orxporter).


---

## Dependencies

- Python 3.6+
- [lxml](https://lxml.de/) (install via pip)
- [fonttools](https://github.com/fonttools/fonttools) (install via pip)

---

## Documentation

#### [How to make a font](docs/howto/howto.md)

#### [FAQ](docs/faq.md)

---

## Compatibility/stability notes

### General stability

forc is very much in development and probably isn't ready for production in any serious task.

The `ttx` compiler (which is an external software called fonttools) will change various metadata elements you put in the manifest to different things. I cannot change this and while I've been working on a custom binary compiler to get around this and other limitations of `ttx`, it's not yet ready to use in production.

At the moment it will always throw some errors about the number of sbix strikes not being the same as maxp.numGlyphs. This is a non-breaking error and you can ignore this.

### Format stability

This is only with the `ttx` compiler - the `forc` compiler is not yet ready for use. Also your mileage may vary depending on your input images and manifest data - fonts are complicated things.

| format | stability | notes |
|:--|:--|:--|
| SVGinOT | sometimes okay | If you have a single SVG with some wrong parts to it (I'm not sure what those are), then the entire font glyph set will just not display. Unfortunately SVGinOT is a really inconsistent and poorly documented format :S. |
| sbixOT | quite stable | This has been tested working within macOS and GNOME in Linux. |
| sbixOT for iOS | quite stable | This has been tested working in iOS 13. |
| CBDT/CBLC | not working | Even though the output is a valid font, glyphs don't display in any compatible environment that has been tested. It's unclear why that is at this point in time. |

---

## Collaborators
- Dzuk
- kiilas (helping out with various things)

---

## Contributions

Feature requests and collaboration are welcome. Any collaborators must follow [Mutant Standard's code of conduct](code_of_conduct.md).

----

## License

forc is licensed under the [Cooperative Non-Violent License (CNPL) v4](license.txt).

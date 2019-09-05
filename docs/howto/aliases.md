# Aliases

Often when making an emoji font, you only tie one codepoint sequence to one glyph, but sometimes you might want more than one.

Alias glyphs let you attach additional codepoint sequences to existing glyphs, so one glyph can have multiple codepoint sequences associated with it.



Alias glyphs are created by a JSON file, which is is structured as follows:


````
{ target : destination
, target : destination
, target : destination
, ...
}

````

The target is the codepoint of the alias glyph, and the destination is the image glyph the alias is pointing to.

The format of the target and destination are exactly the same as the filenames of your [input images](input.md).

````
example

{ "1f3f3-fe0f-200d-26a7" : "101681"
}


````

- Destination sequences must exist in the input folder.
- Target sequence as a whole must **not** already be represented in the input folder.
- All of the parts of every target sequence must be represented by an image glyph or another alias target. 
- The delimiters between codepoints should be identical to your input folder (as the `-d` flag for codepoint delimiters applies to both the aliases file and the input folder).
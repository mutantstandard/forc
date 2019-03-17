# Alias Glyphs
Alias glyphs let you attach additional codepoint sequences to existing glyphs, so one glyph can have multiple codepoint sequences associated with it.



Alias glyphs are created by a JSON file, which is is structured as follows:


````
{ target : destination
, target : destination
, target : destination
...
}

````

'Targets' are the codepoint glyph  sequences, and 'destinations' are existing image glyph sequences.

````
example

{ "1F3F3-FE0F-200D-26A7" : "101681"
}


````

- Destination sequences must exist in the input folder.
- Target sequence as a whole must **not** already be represented in the input folder.
- All of the parts of every target sequence must be represented by an image glyph or another alias target. 
- The delimiters between codepoints should be identical to your input folder (as the `-d` flag for codepoint delimiters applies to both the aliases file and the input folder).
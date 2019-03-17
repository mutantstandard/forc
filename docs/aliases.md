# Alias Glyphs
Alias glyphs let you attach additional codepoint sequences to existing glyphs, so one glyph can have multiple codepoint sequences associated with it.



Alias glyphs are created by a JSON file, which is is structured as follows:


````
{ codepoint seq. of destination glyph : [ list of target codepoint seqs. ]
, ...
}

````


````
example

{ "101681": ["1F3F3-FE0F-200D-26A7"]
}


````

- Your destination glyphs must exist in the input folder.
- The target codepoint sequence itself must **not** already be represented in the input folder.
- All of the parts of your target codepoint sequences must be represented by an existing glyph or alias. 
- The delimiters between codepoints should be identical to your input folder (as the `-d` flag for codepoint delimiters applies to both the aliases file and the input folder).
import re


# validate.data
# ---------------------------
#
# for validating specific miscellaneous user input data types.


# these regexes are designed to find negative results rather than positive ones.
# (this is so the invalid characters can be read back out to the user.)
postScriptNameRegex = "(?=[\[\](){}<>/%])[\u0021-\u007e]"

def validatePostScriptName(string):
    """
    Ensures that a string is compliant with the restricted set of characters required in PostScript names.

    (https://docs.microsoft.com/en-us/typography/opentype/spec/name#name-ids)

    (ASCII codes 33-126 apart from '[', ']', '(', ')', '{', '}', '<', '>', '/', '%')
    (U+21-U+7e, excluding 25, 28, 29, 2f, 3c, 3e, 5b, 5d, 7b, 7d)
    """

    if len(string) > 63:
        raise ValueError("Your PostScript name is more than 63 characters. A PostScript name can be no longer than 63 characters")

    find = re.findall(postScriptNameRegex, string)

    if len(find) > 0:
        raise ValueError(f"Your PostScript name contains the following: {', '.join(find)}. This is not valid. It must only contain certain characters. These include alphanumeric characters and some symbols. Disallowed symbols are '[', ']', '(', ')', '{', '}', '<', '>', '/' and '%'. (In techspeak - only in the unicode range U+21-U+7e, minus the aforementioned symbols.)")

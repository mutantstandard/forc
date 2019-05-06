

def validateAliases(aliases):
    """
    Validates an aliases data object at a basic, structural level.
    """

    if type(aliases) is not dict:
        raise Exception("Your alises file is not structured properly. It needs to be an object type.")

    for target, dest in aliases.items():
        # checking the target isn't necessary because the JSON parser will break if it's not a string.

        if type(dest) is not str:
            raise Exception(f"The destination for the alias '{target}' is not formatted as a string. It needs to be a string.")

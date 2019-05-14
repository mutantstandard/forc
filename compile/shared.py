


def writeFile(path, contents, exceptionString):
    """
    A basic repetitive function that tries to write something to a file.
    """
    try:
        with open(path, 'wb') as file:
            file.write(contents)
    except Exception:
        raise Exception(exceptionString)

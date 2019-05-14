import pathlib
import json



def tryDirectory(absolutePath, dirOrFile, dirName, tryMakeFolder=False):
    """
    Function for checking if a directory exists and/or fulfils certain requirements.
    WIll raise an Exception or ValueError if it doesn't meet these expectations.

    Error printouts designed to reflect internal file operations.
    """
    if not absolutePath.exists():
        if not tryMakeFolder:
            raise ValueError(f"The {dirName} ({absolutePath}) doesn't exist.")
        else:
            try:
                absolutePath.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise Exception(f"Couldn't make the {dirName} ({absolutePath}). ({e})" )
    else:
        if dirOrFile == "file" and absolutePath.is_dir():
                raise ValueError(f"{dirName} ({absolutePath}) is a folder, not a file.")
        elif dirOrFile == "dir" and absolutePath.is_file():
                raise ValueError(f"{dirName} ({absolutePath}) is a file, not a folder.")



def tryUserDirectory(absolutePath, dirOrFile, dirName, tryMakeFolder=False):
    """
    Function for checking if a directory exists and/or fulfils certain requirements.
    WIll raise an Exception or ValueError if it doesn't meet these expectations.

    With error printouts designed to reflect end-user inputs.
    """

    if not absolutePath.exists():
        if not tryMakeFolder:
            raise ValueError(f"The {dirName} you gave ({absolutePath}) doesn't exist.")
        else:
            try:
                absolutePath.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise Exception(f"Couldn't make the {dirName} ({absolutePath}). ({e})" )
    else:
        if dirOrFile == "file" and absolutePath.is_dir():
                raise ValueError(f"The {dirName} you gave ({absolutePath}) is a folder, not a file.")
        elif dirOrFile == "dir" and absolutePath.is_file():
                raise ValueError(f"The {dirName} you gave ({absolutePath}) is a file, not a folder.")



def loadJson(jsonPath, fileName):
    """
    Repetitive function for attempting to load a JSON file.
    """
    try:
        with open(jsonPath, "r") as read_file:
            return json.load(read_file)
    except Exception as e:
        raise ValueError(f"Loading the {fileName} file failed! ({e})")



def writeFile(path, contents, exceptionString):
    """
    A basic repetitive function that tries to write something to a file.
    """
    try:
        with open(path, 'wb') as file:
            file.write(contents)
    except Exception:
        raise Exception(exceptionString)

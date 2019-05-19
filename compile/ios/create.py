import subprocess
import pathlib
import log

import files
from compile.ios.assembler import compileiOSConfig



def createPackage(formatData, filename, outputPath, fontPath, manifest):

    # iOS Configuration Profile compilation
    # (must come after everything else)
    log.out(f'Compiling iOS Configuration Profile...')
    configString = compileiOSConfig(manifest, fontPath, outputPath)
    configPath = outputPath / (f"{filename}.mobileconfig")
    files.writeFile(configPath, configString, 'Could not write iOS Configuration Profile to file')

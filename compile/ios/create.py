import subprocess
import pathlib
import log

from compile.shared import writeFile
from compile.ios.assembler import compileiOSConfig



def createPackage(formatData, filename, outputPath, outputFontPath, manifest):

    outputFontPath = outputPath / (filename + formatData['extension'])

    # iOS Configuration Profile compilation
    # (must come after everything else)
    log.out(f'Compiling iOS Configuration Profile...')
    configString = compileiOSConfig(manifest, outputFontPath, outputPath)
    configPath = outputPath / (f"{filename}.mobileconfig")
    writeFile(configPath, configString, 'Could not write iOS Configuration Profile to file')

    log.out(f'🗑  Deleting the original Font...')
    outputFontPath.unlink() #delete

    log.out(f'✅ This font has been successfully created.\n\n', 32)

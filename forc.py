#!/usr/bin/env python3

import getopt
import os
import sys
from io import StringIO

import log
from export import export



VERSION = '0.0.1'

DEF_INPUT_PATH = 'in'
DEF_OUTPUT_PATH = 'out'
DEF_MANIFEST = 'manifest.json'
DEF_ALIASES = None

DEF_OUTPUT_FORMATS = ['SVGinOT']
DEF_DELIM_CODEPOINT = "-"

DEF_TTX_OUTPUT = False
DEF_DEV_TTX = False

DEF_NO_VS16 = False
DEF_NUSC = False
DEF_NFCC = False

DEF_NO_LIG = False




HELP = f'''forc {VERSION}
by Mutant Standard
(mutant.tech)

USAGE: forc.py [options...]

OPTIONS:

-h      Prints this help message.

-i      Image glyphs directory (default: {DEF_INPUT_PATH})
-a      Alias glyphs file (optional)
-m      Manifest file (default: {DEF_MANIFEST})
-o      Output directory (default: {DEF_OUTPUT_PATH})


-F      Format (default: {DEF_OUTPUT_FORMATS})

        Formats that require SVG images:
        - SVGinOT       (Many platforms)

        Formats that require PNG images:
        - sbixTT        (macOS)
        - sbixOT
        - sbixTTiOS     (iOS)
        - sbixOTiOS     (DEVELOPMENT/TESTING)
        - CBx           (Google/Android)


-d      Delimiter between ligatured codepoints
        (default: '{DEF_DELIM_CODEPOINT}')




--ttx       Exports a matching ttx (.ttx) file for each format.

--dev-ttx   Keeps the initial ttx that forc compiles before
            passing it to fonttools. This is different to the above,
            which is a full representation of the font file.




--no-vs16   Strips any presence of VS16 (U+fe0f) from the output.

--nusc      No Unenforced SVG Contents Checking.
            Makes SVG checking less strict, by only checking SVG
            parts that are explicitly not allowed in SVGinOT.

--nfcc      No File Consistency Checking.
            Stops forc from checking if the images in the format
            subfolders are all the same. Useful if you have made
            guarantees beforehand and want to save time.



--no-lig    (DEVELOPMENT OPTION) Strips ligatures from the output.






look at docs/howto.md for more information on how to use many of these.

'''



def main():
    input_path = DEF_INPUT_PATH
    output_path = DEF_OUTPUT_PATH
    manifest_path = DEF_MANIFEST
    aliases_path = DEF_ALIASES

    output_formats = DEF_OUTPUT_FORMATS
    delim_codepoint = DEF_DELIM_CODEPOINT

    ttx_output = DEF_TTX_OUTPUT
    dev_ttx_output = DEF_DEV_TTX

    no_vs16 = DEF_NO_VS16
    nusc = DEF_NUSC
    nfcc = DEF_NFCC

    no_lig = DEF_NO_LIG


    try:
        opts, _ = getopt.getopt(sys.argv[1:],
                                'hi:o:m:a:F:d:',
                                ['help', 'ttx', 'dev-ttx', 'no-vs16', 'nusc', 'nfcc', 'no-lig'])
        for opt, arg in opts:
            if opt in ['-h', '--help']:
                print(HELP)
                sys.exit()
            elif opt == '-i':
                input_path = arg
            elif opt == '-o':
                output_path = arg
            elif opt == '-m':
                manifest_path = arg
            elif opt == '-a':
                aliases_path = arg
            elif opt == '-F':
                output_formats = arg.split(',')
            elif opt =='-d':
                delim_codepoint = arg

            elif opt =='--ttx':
                ttx_output = True
            elif opt =='--dev-ttx':
                dev_ttx_output = True


            elif opt =='--no-vs16':
                no_vs16 = True
            elif opt =='--nusc':
                nusc = True
            elif opt =='--nfcc':
                nfcc = True

            elif opt =='--no-lig':
                no_lig = True

    except Exception:
        print(HELP)
        sys.exit(2)
    try:
        export( input_path
              , output_path
              , manifest_path
              , aliases_path
              , output_formats
              , delim_codepoint

              , ttx_output
              , dev_ttx_output

              , no_vs16
              , nusc
              , nfcc

              , no_lig
              )

    except Exception as e:
        log.out(f'!!! {e}', 31)
        raise e  ######################## TEMP
        sys.exit(1)
    log.out('All done!', 35)

if __name__ == '__main__':
    main()

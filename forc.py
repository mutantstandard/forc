#!/usr/bin/env python3

import getopt
import os
import sys
from io import StringIO

import log
from export import export



VERSION = '0.0.1'
DEF_MANIFEST = 'manifest.json'
DEF_INPUT_PATH = 'in'
DEF_OUTPUT_PATH = 'out'
DEF_OUTPUT_FORMATS = ['SVGinOT']
DEF_TTX_OUTPUT = False
DEF_DEV_TTX = False
DEF_DELIM_CODEPOINT = "-"

DEF_NO_LIG = False
DEF_NO_VS16 = False
DEF_NFCC = False

HELP = f'''forc {VERSION}
by Mutant Standard
(mutant.tech)

USAGE: forc.py [options...]

OPTIONS:

-h      Prints this help message.

-i      Input directory (default: {DEF_INPUT_PATH})
-o      Output directory (default: {DEF_OUTPUT_PATH})
-m      Manifest file (default: {DEF_MANIFEST})


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

--ttx       Export a matching ttx (.ttx) file for each format.

--dev-ttx   Keep the initial ttx that forc compiles before
            passing it to fonttools. This is different to the above,
            which is a full representation of the font file..

--no-lig    (DEVELOPMENT OPTION) Strip ligatures from the output.

--no-vs16   (DEVELOPMENT OPTION) Strip any presence of VS16 (U+fe0f)
            from the output.

--nfcc      (DEVELOPMENT OPTION) No File Consistency Checking.
            Stops forc from checking if the images in the format
            subfolders are all the same.



look at docs/howto.md for more information on how to use many of these.

'''



def main():
    manifest_path = DEF_MANIFEST
    input_path = DEF_INPUT_PATH
    output_path = DEF_OUTPUT_PATH
    output_formats = DEF_OUTPUT_FORMATS
    ttx_output = DEF_TTX_OUTPUT
    dev_ttx_output = DEF_DEV_TTX
    delim_codepoint = DEF_DELIM_CODEPOINT

    no_lig = DEF_NO_LIG
    no_vs16 = DEF_NO_VS16
    nfcc = DEF_NFCC

    try:
        opts, _ = getopt.getopt(sys.argv[1:],
                                'hm:i:o:F:d:',
                                ['help', 'ttx', 'dev-ttx', 'no-lig', 'no-vs16', 'nfcc'])
        for opt, arg in opts:
            if opt in ['-h', '--help']:
                print(HELP)
                sys.exit()
            elif opt == '-m':
                manifest_path = arg
            elif opt == '-i':
                input_path = arg
            elif opt == '-o':
                output_path = arg
            elif opt == '-F':
                output_formats = arg.split(',')
            elif opt =='-d':
                delim_codepoint = arg
            elif opt =='--ttx':
                ttx_output = True
            elif opt =='--dev-ttx':
                dev_ttx_output = True
            elif opt =='--no-lig':
                no_lig = True
            elif opt =='--no-vs16':
                no_vs16 = True
            elif opt =='--nfcc':
                nfcc = True

    except Exception:
        print(HELP)
        sys.exit(2)
    try:
        export( manifest_path
              , input_path
              , output_path
              , output_formats
              , delim_codepoint
              , ttx_output
              , dev_ttx_output
              , no_lig
              , no_vs16
              , nfcc
              )

    except Exception as e:
        log.out(f'!!! {e}', 31)
        raise e  ######################## TEMP
        sys.exit(1)
    log.out('All done', 35)

if __name__ == '__main__':
    main()

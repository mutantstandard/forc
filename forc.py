#!/usr/bin/env python3

import getopt
import os
import sys
import json
from io import StringIO

import log
from export import export



VERSION = '0.0.0'
DEF_MANIFEST = 'manifest.json'
DEF_INPUT_PATH = 'in'
DEF_OUTPUT_PATH = 'out'
DEF_OUTPUT_FORMATS = ['svginot']
DEF_TTX_OUTPUT = False
DEF_DEV_TTX = False
DEF_DELIM = "-"

HELP = f'''forc {VERSION}
USAGE: forc.py [options...]

OPTIONS:
-h      prints this help message

-m      input JSON manifest (default: {DEF_MANIFEST})
-i      input directory path (default: {DEF_INPUT_PATH})
-o      output (default: {DEF_OUTPUT_PATH})

-F      format (default: {DEF_OUTPUT_FORMATS})
        (svginot, sbix, sbixios, cbx)
        (.otf, .ttf, .ttf, .mobileconfig)
        (default: svginot)

-d      delimiter between chained Unicode codepoints
        (default: {DEF_DELIM})

--ttx       export an additional ttx (.ttx) file for each format
--dev-ttx   keep the original ttx that forc compiles before passing it to fonttools

'''



def main():
    manifest_path = DEF_MANIFEST
    input_path = DEF_INPUT_PATH
    output_path = DEF_OUTPUT_PATH
    output_formats = DEF_OUTPUT_FORMATS
    ttx_output = DEF_TTX_OUTPUT
    dev_ttx_output = DEF_DEV_TTX
    delim = DEF_DELIM

    try:
        opts, _ = getopt.getopt(sys.argv[1:],
                                'hm:i:o:F:d:',
                                ['help', 'ttx', 'dev-ttx'])
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
                delim = arg
            elif opt =='--ttx':
                ttx_output = True
            elif opt =='--dev-ttx':
                dev_ttx_output = True

    except Exception:
        print(HELP)
        sys.exit(2)
    try:
        with open(manifest_path, "r") as read_file:
            m = json.load(read_file)

        export(m, input_path, output_path, output_formats, delim, ttx_output, dev_ttx_output)

    except Exception as e:
        log.out(f'!!! {e}', 31)
        raise e  ######################## TEMP
        sys.exit(1)
    log.out('All done', 35)

if __name__ == '__main__':
    main()

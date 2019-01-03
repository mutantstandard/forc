#!/usr/bin/env python3

import getopt
import os
import sys

import log
from export import export



VERSION = '0.0.0'
DEF_MANIFEST = 'manifest'
DEF_INPUT_PATH = 'in'
DEF_OUTPUT_PATH = 'out'
DEF_OUTPUT_FORMATS = ['svginot']



HELP = f'''forc {VERSION}
USAGE: forc.py [options...]

OPTIONS:
-h      prints this help message

-m      input JSON manifest (default: {DEF_MANIFEST})
-i      input directory path (default: {DEF_INPUT_PATH})
-o      output (default: {DEF_OUTPUT_PATH})

-F      format (default: {DEF_OUTPUT_FORMATS})
        (svginot, sbix, cbdtcblc, sbixios)
        (.otf, .ttf, .ttf, .mobileconfig)


'''



def main():
    manifest_path = DEF_MANIFEST
    input_path = DEF_INPUT_PATH
    output_path = DEF_OUTPUT_PATH
    output_formats = DEF_OUTPUT_FORMATS

    try:
        opts, _ = getopt.getopt(sys.argv[1:],
                                'hm:i:o:F:',
                                ['help'])
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
    except Exception:
        print(HELP)
        sys.exit(2)
    try:
        log.out(f'Loading manifest file...', 36)
        m = manifest.Manifest(os.path.dirname(manifest_path),
                              os.path.basename(manifest_path))
        print(export(m, input_path, output_formats))
    except Exception as e:
        log.out(f'!!! {e}', 31)
        sys.exit(1)
    log.out('All done', 36)

if __name__ == '__main__':
    main()

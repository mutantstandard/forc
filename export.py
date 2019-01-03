from assembler import assembler

def export(m, inputPath, outputFormats, outputPath):

    ttx = assembler()

    # feed the assembled TTX as input to the ttx commaand line tool.
    cmd_png = ['ttx', ttx, '-o', outputPath]

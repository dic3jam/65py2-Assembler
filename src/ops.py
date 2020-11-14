import sys

def checkThenOpen(argv):
    '''
    Ensures that only one file with an extension of
    .asm or .s has been passed to the program
    
    Parameters
    -------------
    argv: list
        the command line arguments passed to the program

    Returns
    ------------
    readFile
        a file object in "r" mode of the assembly
        file to be processed
    '''

    if(len(sys.argv) > 2):
        print("Too many arguments")
        sys.exit(1)

    inputFile = sys.argv[1]

    if not inputFile.lower().endswith(('.s', '.asm')): 
        print("Must be a .s or .asm file")
        sys.exit(1)

    readFile = open(inputFile, "r")

    return readFile


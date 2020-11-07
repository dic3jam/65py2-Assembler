import sys

def checkThenOpen(argv):

    if(len(sys.argv) > 2):
        print("Too many arguments")
        sys.exit(1)

    inputFile = sys.argv[1]

    if not inputFile.lower().endswith(('.s', '.asm')): 
        print("Must be a .s or .asm file")
        sys.exit(1)

    readFile = open(inputFile, "r")

    return readFile


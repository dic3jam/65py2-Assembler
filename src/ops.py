import sys
from src.opcodes import *

"""
65py2 Ops
------------------
A collection of basic operations to
support the assembler

Methods:
------------------

checkThenOpen:
    Ensures that only one file with an extension of
    .asm or .s has been passed to the program

get_opcode_hex:
    gets the hexadecimal code
    for the inputted opcode
"""


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
    readFile: file
        a file object in "r" mode of the assembly
        file to be processed
    '''

    if(len(sys.argv) > 2):
        print("Too many arguments")
        sys.exit(1)

    try:
        inputFile = sys.argv[1]
    except IndexError:
        print("Must provide one assembly file to assemble")
        sys.exit(1)
    except FileNotFoundError:
        print("That assembly file does not exist")
        sys.exit(1)

    if not inputFile.lower().endswith(('.s', '.asm')):
        print("Must be a .s or .asm file")
        sys.exit(1)

    readFile = open(inputFile, "r")

    return readFile


def get_opcode_hex(opcode, add):
    '''
    gets the hexadecimal code
    for the inputted opcode

    Parameters
    -------------
    opcode: str
        the opcode to search for

    addressing: str
        the addressing type to index
        into

    Returns
    ------------
    the hexadecimal code of that opcode
    for the addressing specified
    '''
    try:
        x = opcodes_list.index(add)
        return opcodes_list[x][opcode]
    except KeyError:
        print(opcode + " cannot be addressed that way")
        sys.exit(1)


def swriter(functions):
    '''
    Writes the data structures out to
    a .bin file that can be executed
    on the target processor

    Parameters:
    --------------
    functions: dict
        the dictionary of functions
        will be written in order to
        the .bin file
    '''
    with open("a.bin", "wb") as out:
        for func in functions:
            out.write(bytes(functions[func]))
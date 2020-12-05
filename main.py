'''65py2 - A 6502 Assembler'''
import sys
from src.opcodes import *
from src.ops import *
from src.sreader import *

# Global Variables

# keeps track of the number of times we have to splt a value over
# over 255 - important for getting the correct program counter position
# when applying the jump instruction 
splitz = 0

def main():
    readFile = checkThenOpen(sys.argv)
    assignments = find_assignments(readFile)
    functions, splits = function_reader(readFile, assignments, opcodes_list, splitz)
    readFile.close()
    jmp_function(splits)
    swriter(functions)


main()
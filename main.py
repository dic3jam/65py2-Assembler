'''65py2 - A 6502 Assembler'''
import sys
from src.opcodes import *
from src.ops import *
from src.sreader import *

def main():
    readFile = checkThenOpen(sys.argv)
    assignments = find_assignments(readFile)
    functions = function_reader(readFile, assignments, opcodes_list)
    readFile.close()
    jmp_function()
    swriter(functions)


main()

'''65py2 - A 6502 Assembler'''
import sys
from src.ops import *
from src.sreader import *

def main():
    readFile = checkThenOpen(sys.argv)
    assignments = find_assignments(readFile)
    functions, program_counter, jmp_list = sreader(readFile, assignments)
    functions, program_counter = prune_functions(functions, program_counter)
    functions, program_counter = jmp_function(functions, program_counter, jmp_list)
    readFile.close()
    swriter(functions)


main()

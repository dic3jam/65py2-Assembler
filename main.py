'''65py2 - A 6502 Assembler'''

from src.opcodes import opcodes_list
from src.ops import *
from src.sreader import *

readFile = checkThenOpen(sys.argv)

assignments = find_assignments(readFile)

print(assignments)

functions = function_reader(readFile, assignments, opcodes_list)

print(functions)






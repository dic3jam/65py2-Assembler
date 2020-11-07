'''65py2 - A 6502 Assembler'''

from src.opcodes import *
from src.ops import *
from src.sreader import *

readFile = checkThenOpen(sys.argv)

assignments = find_assignments(readFile)

print(assignments)

#functions = find_functions(readFile, assignments, opcodes)






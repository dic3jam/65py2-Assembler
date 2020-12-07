import re
import sys
from src.jmp_ins import jmp_ins
from src.ops import *
from src.opcodes import *

# TODO
'''
finish addressing modes in command reader
'''

"""
65py2 Reader
--------------------
A collection of functions for
processing 6502 Assembly files
into data structures

Methods:
--------------------

find_assignments:
    Scans through the assembly file and
    creates a dictionary of the variables
    and their assignments

num_types:
    Identifies a binary, hexadecimal,
    decimal number, a variable, or a function
    header as a variable. Returns the corresponding
    value as an integer.

jmp_function:
    iterates through jmp_ins objects to assign them to the
    program

function_reader:
    Iterates through the file and builds the functions
    dictionary by assigning the function header as the key
    and a list of the values and opcodes as the value

command_reader:
    Identifies the opcode used in a line,
    sorts through the addressing modes and
    returns the correct hex for the opcode

prune_functions:
    iterates through the functions dict
    splits values > 255 into little endian
    format. Updates the program counter

inc_counter:
    Adds the symbol (opcode, value, variable)
    to the program counter - builds an index
    of the position of items in the
    assembly file
"""

# Regular expressions for pattern matching

# Determines if a line is attempting to assign a variable a value
assignment = re.compile(r"(^[a-zA-Z0-9]+)\s?[=]\s?(\$[a-fA-F0-9]{2,4}|\%[0-1]{8}|[^a-zA-Z]\d+)")
# The variable being assigned
assign = re.compile(r"\#?^[a-zA-Z0-9]+")
# The value being assigned to the variable
num = re.compile(r"\#?\$[a-fA-F0-9]{2,4}|\#?\%[0-1]{8}|\#?[^a-zA-Z]\d+")
# matches a binary number
binary = re.compile(r"\%([0-1]{8})")
# matches a hexadecimal value
hexadecimal = re.compile(r"\$([a-fA-F0-9]{2,4})")
# matches a decimal value
decimal = re.compile(r"[^a-zA-Z](\d+)")
# determines if a line is a function header
function_header = re.compile("(\w+)\:")
# command = re.compile(r"\t(\w+)\s(\$[a-fA-F0-9]{2,4}|\%[0-2]{8}|[0-2]\d{2})")
# Determines if a line is an opcode
opcode = re.compile(r"\t(\w{3})")
# identifies an action for an opcode
action = re.compile(r"\t\w{3}\s\#?(\%?\$?\w+)")
# determines the use of immediate addressing
immediate = re.compile(r"\#")


def find_assignments(readFile):
    '''
    Scans through the assembly file and
    creates a dictionary of the variables
    and their assignments

    Parameters:
    ---------------
    readFile: file
        the open assembly file, not null

    Returns:
    ---------------
    A dictionary that contains variables
    and their values
    '''
    assignments = {}
    # iterate and assign to dictionary
    for line in readFile:
        if(re.match(assignment, line)):
            # get left name as string
            left = assign.findall(line)[0]
            # get right side
            right = num_type(num.findall(line)[0], assignments)
            # add assignment to data structure
            assignments[left] = right
    readFile.seek(0)
    return assignments


def sreader(readFile, assignments):
    '''
    Iterates through the file and builds the functions
    dictionary by assigning the function header as the key
    and a list of the values and opcodes as the value

    Parameters:
    ----------------
    readFile: file
        the assembly file

    assignments: dictionary
        dictionary with the variables and
        values

    opcodes_list: list
        list containing the dictionaries of opcodes

    Returns
    -----------------
    the functions dict complete with each function and
    its corresponding opcodes/values in a list
    '''
    functions = {}
    program_counter = []
    jmp_list = []
    header_count = 0
    # iterate through the file
    for line in readFile:
        # if the line is a function header
        if re.match(function_header, line):
            # increment the counter
            header_count += 1
            # create a list to capture the opcodes and values
            func_bytelist = []
            # get its name
            name = function_header.findall(line)[0]
            # add to the program counter
            program_counter.append(name)
            bytelist_add, program_counter, jmp_list = function_reader(readFile,
                            assignments, program_counter, jmp_list, header_count, name)
            func_bytelist.extend(bytelist_add)
            functions[name] = func_bytelist
        else:
            continue
    # reset the file position
    readFile.seek(0)
    functions, program_counter = prune_functions(functions, program_counter)

    return functions, program_counter, jmp_list


def function_reader(readFile, assignments, program_counter, jmp_list, count, name):
    func_bytelist = []
    for line in readFile:
        if re.search(opcode, line):
            line_command = command_reader(line)
            func_bytelist.append(line_command)
            program_counter.append(line_command)
        # if there is number or assignment after the opcode, get that
        # and add to the bytearray
        if re.search(action, line):
            num = num_type(line, assignments)
            # if the command is a jmp or jsr command
            if line_command == 0x4c or line_command == 0x20:
                new_jmp, func_bytelist, program_counter = add_jmp(
                       name, program_counter, func_bytelist, count, num)
                jmp_list.append(new_jmp)
            else:
                func_bytelist.append(num)
                program_counter.append(num)

        # once through the whole file, assign the function name
        # and the bytearray to the dictionary
        if re.match(r"\n", line):
            return func_bytelist, program_counter, jmp_list
        else:
            continue


def add_jmp(name, program_counter, func_bytelist, count, num):
    pos_counter = len(program_counter) - count
    pos_func = len(func_bytelist) - 1
    new_jmp = jmp_ins(name, pos_counter, pos_func, num)
    for x in range(2):
        func_bytelist.append(0x00)
        program_counter.append(0x00)

    return new_jmp, func_bytelist, program_counter


def num_type(line, assignments):
    '''
    Identifies a binary, hexadecimal,
    decimal number, a variable, or a function
    header as a variable. Returns the corresponding
    value as an integer.

    Parameters
    -------------------
    line: string
        the line we are currently iterating through

    Returns
    ------------------
    the value of the number, variable
    if the num is > 0xFFFF, then return 0xEA (nop)
    if in error, return 0xEA
    '''
    # If it is a binary number, return it
    if re.search(binary, line):
        return bin_return(line)
# if it is a hexadecimal number, return it
    elif re.search(hexadecimal, line):
        return hex_return(line)
# if it is a decimal number, return it
    elif re.search(decimal, line):
        return dec_return(line)
# otherwise if it is a variable, search in that dictionary
    # and return the corresponding value
    var = action.findall(line)[0]

    if var in assignments:
        return assignments[var]
    # else it is a function header for a jmp or jsr ins
    else:
        return var


def bin_return(line):
    Bin = binary.findall(line)[0]
    if int(Bin, 2) < 0xFFFF:
        return int(Bin, 2)
    else:
        return 0xEA


def hex_return(line):
    Hex = hexadecimal.findall(line)[0]
    if int(Hex, 16) < 0xFFFF:
        return int(Hex, 16)
    else:
        return 0xEA


def dec_return(line):
    Dec = decimal.findall(line)[0]
    if int(Dec) < 0xFFFF:
        return int(Dec)
    else:
        return 0xEA


def command_reader(line):
    '''
    Identifies the opcode used in a line,
    sorts through the addressing modes and
    returns the correct hex for the opcode

    Parameters
    --------------
    line: string
        the line we are analyzing
    opcodes_list: dict
        the list of dicts organizing opcodes
        by addressing mode

    Returns
    --------------
    integer of the value of the desired
    opcode

    Notes
    -------------
    Opcodes in V1:
    accumulator
    immediate
    absolute
    implied
    relative
    '''
    # get the command
    left = opcode.findall(line)[0]
    # get the action, if there is no action
    # then it is accumulator or implied addressing
    try:
        action.findall(line)[0]
    except IndexError:
        if left in acc:
            return get_opcode_hex(left, acc)
        elif left in imp:
            return get_opcode_hex(left, imp)

    # if the line contains a # it is immediate
    if(re.search(immediate, line)):
        return get_opcode_hex(left, imm)
    # check other addressing dicts
    elif left in rel:
        return get_opcode_hex(left, rel)
    elif left in abso:
        return get_opcode_hex(left, abso)


def get_opcode_hex(opcode, add):
    '''
    gets the hexadecimal code
    for the inputted opcode

    Parameters
    -------------
    opcode: str
        the opcode to search for

    add: str
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

import re
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

# Make some regular expressions for pattern matching
# Determines if a line is attempting to assign a variable a value
assignment = re.compile(r"(^[a-zA-Z0-9]+)\s?[=]\s?(\$[a-fA-F0-9]{2,4}|\%[0-1]{8}|[^a-zA-Z]\d+)")
# The variable being assigned
assign = re.compile(r"^[a-zA-Z0-9]+")
# The value being assigned to the variable
num = re.compile(r"\#?\$[a-fA-F0-9]{2,4}|\%[0-1]{8}|[^a-zA-Z]\d+")
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
action = re.compile(r"\t\w{3}\s(\#?\%?\$?\w+)")
# determines the use of immediate addressing
immediate = re.compile(r"\#")

# Data Structures

# variables and their values
assignments = {}
# the index of each item in the list represents its
# position to the program counter
program_counter = []
# each function is stored with the key as the function header
# and the opcodes and values stored as a list of values
functions = {}
# contains the jmp_ins objects capturing the details related to
# jmp or jsr commands
jmp_list = []


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
        Bin = binary.findall(line)[0]
        if int(Bin, 2) < 0xFFFF:
            return int(Bin, 2)
        else:
            return 0xEA
    # if it is a hexadecimal number, return it
    elif re.search(hexadecimal, line):
        Hex = hexadecimal.findall(line)[0]
        if int(Hex, 16) < 0xFFFF:
            return int(Hex, 16)
        else:
            return 0xEA
    # if it is a decimal number, return it
    elif re.search(decimal, line):
        Dec = decimal.findall(line)[0]
        if int(Dec) < 0xFFFF:
            return int(Dec)
        else:
            return 0xEA
    # otherwise if it is a variable, search in that dictionary
    # and return the corresponding value
    var = action.findall(line)[0]
    if var in assignments:
        return assignments[var]
    # else it is a function header for a jmp or jsr ins
    else:
        return var


def jmp_function():
    '''
    Iterates through jmp_ins objects to assign them to the
    program. If destination function does not exist, will
    "jump" to the current position in the program

    Parameters:
    ----------------
    jmp_list: list
        list containing all jmp_ins objects

    Modifies:
    ----------------
    the functions dict and program counter to contain
    the assembly files jmp or jsr instructions
    '''
    # if there were no jmp or jsr instructions, skip
    if len(jmp_list) == 0:
        return
    # iterate through the jmp_ins objects
    for jmp in jmp_list:
        # determine the final destination in little endian
        jmp.dest_pos(program_counter)
        # insert the low byte after the opcode
        functions[jmp.orig_name][jmp.pos_func + 1] = jmp.lo_byte
        # insert the high byte after the low byte
        functions[jmp.orig_name][jmp.pos_func + 2] = jmp.hi_byte
        # dothe same for the program counter
        program_counter[jmp.pos_counter + 1] = jmp.lo_byte
        program_counter[jmp.pos_counter + 2] = jmp.hi_byte


def function_reader(readFile, assignments, opcodes_list):
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

    Returns:
    -----------------
    the functions dict complete with each function and
    its corresponding opcodes/values in a list
    '''
    # iterate through the file
    for line in readFile:
        # create a list to capture the opcodes and values
        func_bytelist = []
        # if the line is a function header
        if re.match(function_header, line):
            # get its name
            name = function_header.findall(line)[0]
            # add to the program counter
            inc_counter(name)
            for line in readFile:
                # so long as we do not encounter a blank line or another function
                # if you find an opcode, get its correct hex code and
                # add to the bytearray
                if re.search(opcode, line):
                    line_command = command_reader(line, opcodes_list)
                    func_bytelist.append(line_command)
                    inc_counter(line_command)
                # if there is number or assignment after the opcode, get that
                # and add to the bytearray
                if re.search(action, line):
                    num = num_type(line, assignments)
                    if line_command == 0x4c or line_command == 0x20:
                        pos_counter = len(program_counter) - 1
                        pos_func = len(func_bytelist) - 1
                        jmp_list.append(jmp_ins(name, pos_counter,
                                        pos_func, num))
                        for x in range(2):
                            func_bytelist.append(0x00)
                            program_counter.append(0x00)
                        continue
                    func_bytelist.append(num)
                    inc_counter(num)
                # once through the whole file, assign the function name
                # and the bytearray to the dictionary
                if re.match(r"\n", line):
                    functions[name] = func_bytelist
                    break
                '''
                TODO nested functions
                if re.match(function_header, line):
                    functions[name] = func_bytelist
                    try:
                        sub_name = function_header.findall(line)[0]
                    except IndexError:
                        pass # TODO think of something better
                    sub_function = function_reader(readFile, assignments, opcodes_list)
                    functions[sub_name].insert(sub_function[sub_name])
                    break
                '''
    # reset the file position
    readFile.seek(0)
    prune_functions(functions, program_counter)
    return functions


def command_reader(line, opcodes_list):
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
    

def prune_functions(functions, program_counter):
    '''
    iterates through the functions dict
    splits values > 255 into little endian
    format. Updates the program counter

    Parameters:
    --------------
    functions: dict
        the dict of functions and their
        opcodes/values
    '''
    for func in functions:
        for val in functions[func]:
            if val > 255:
                # get the low byte
                low_byte = val & 0b11111111
                # get the high byte
                hi_byte = val >> 8

                # update the functions array

                # determine which index that value is in the
                # functions dict
                index = functions[func].index(val)
                # assign the low byte to val position
                functions[func][index] = low_byte
                # insert the hi_byte after the low_byte
                # shift the rest of the list down
                functions[func].insert((index+1), hi_byte)

                # update the program counter

                # determine the index of the function
                ind_func = program_counter.index(func)
                # use that as a starting point to find the val index
                pro_ind = program_counter.index(val, ind_func)
                # at the former position of val, assign the low_byte
                program_counter[pro_ind] = low_byte
                # at the +1 position of low_byte, assign the hi_byte
                program_counter.insert((pro_ind+1), hi_byte)


def inc_counter(symbol):
    '''
    adds the symbol (opcode, value, variable)
    to the program counter - builds an index
    of the position of items in the
    assembly file

    Parameters
    --------------
    symbol: string, int
        the function header, opcode, or
        value to add
    '''
    program_counter.append(symbol)

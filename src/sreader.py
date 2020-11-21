import re
from src.ops import *
from src.opcodes import *

# TODO
'''
will need a way to format addresses in little endian for full 16 bitaddresses - needed to provide program counter index for jmp
finish jsr_function
finish jmp_function
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

jsr_function: TODO
    Scans through the program for jsr instructions
    modifies the functions dict as well as the program
    counter

jmp_function: TODO
    Processes a jump instruction by inserting
    the corresponding program counter position
    to the functions dict, and appends the
    program counter

function_reader:
    Iterates through the file and builds the functions
    dictionary by assigning the function header as the key
    and a list of the values and opcodes as the value

command_reader:
    Identifies the opcode used in a line,
    sorts through the addressing modes and
    returns the correct hex for the opcode

inc_counter:
    Adds the symbol (opcode, value, variable)
    to the program counter - builds an index
    of the position of items in the
    assembly file
"""

# Make some regular expressions for pattern matching
# Determines if a line is attempting to assign a variable a value
assignment = re.compile(r"(^[a-zA-Z0-9]+)\s?[=]\s?(\$[a-fA-F0-9]{2,4}|\%[0-1]{8}|[0-2]\d{2})")
# The variable being assigned
assign = re.compile(r"^[a-zA-Z0-9]+")
# The value being assigned to the variable
num = re.compile(r"\#?\$[a-fA-F0-9]{2,4}|\%[0-1]{8}|[0-2]\d{2}")
# matches a binary number
binary = re.compile(r"\%([0-1]{8})")
# matches a hexadecimal value
hexadecimal = re.compile(r"\$([a-fA-F0-9]{2,4})")
# matches a decimal value
decimal = re.compile(r"(\d+)")
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
            right = num_type(num.findall(line)[0])
            # add assignment to data structure
            assignments[left] = right
    readFile.seek(0)
    return assignments


def num_type(line):
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
    '''
    # If it is a binary number, return it
    if re.search(binary, line):
        Bin = binary.findall(line)[0]
        return int(Bin, 2)
    # if it is a hexadecimal number, return it
    elif re.search(hexadecimal, line):
        Hex = hexadecimal.findall(line)[0]
        return int(Hex, 16)
    # if it is a decimal number, return it
    elif re.search(decimal, line):
        Dec = decimal.findall(line)[0]
        return int(Dec)
    # otherwise if it is a variable, search in that dictionary
    # and return the corresponding value
    else:
        try:
            assigning = action.findall(line)[0]
        except IndexError:
            return -1
        for x in assignments:
            if x == assigning:
                return assignments[x]


def jmp_function(fnc_header):
    '''
    Processes a jump instruction by inserting
    the corresponding program counter position
    to the functions dict, and appends the
    program counter

    Parameters:
    ----------------
    fnc_header: string
        the function header corresponding to the
        jmp command
    '''
    # TODO
    # if the num position is a function
    # return the contents
    # for y in functions:


def jsr_function(fnc_header):
    '''
    Scans through the program for jsr instructions
    modifies the functions dict as well as the program
    counter

    Parameters:
    ----------------
    fnc_header: string
        the function header corresponding to the
        jmp command

    Modifies:
    ----------------
    The functions dict to insert the subroutines
    to the corresponding function
    '''
    # TODO
    # will be 3rd scan through file


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
                    num = num_type(line)
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
    indirect
    relative
    '''
    # get the command
    left = opcode.findall(line)[0]
    # get the action, if there is no action
    # then it is accumulator addressing
    try:
        action.findall(line)[0]
    except IndexError:
        x = get_opcode_hex(left, acc)

    # if the line contains a # it is immediate
    if(re.search(immediate, line)):
        x = get_opcode_hex(left, imm)
    else:
        # make a list of dictionaries with unique
        # opcodes and iterate through them
        uniq_addressing = [ind, rel, imp]
        for dic in uniq_addressing:
            for op in dic:
                if op == left:
                    x = dic[op]
                    break
        # can only get away with this for now
        # TODO continue to build in other
        # addressing modes
        else:
            for op in abso:
                if op == left:
                    x = abso[op]
                    break
            else:
                x = -1

    return x


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

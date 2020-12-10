import sys
import re
from src.opcodes import *
from src.sreader import function_header

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

swriter:
    Writes the data structures out to
    a .bin file that can be executed
    on the target processor

prune_functions:
    iterates through the functions dict
    splits values > 255 into little endian
    format. Updates the program counter

prune_func:
    Helper function to prune_functions. Inserts
    the hi_byte and low_byte to their positions
    in the functions dict.

prune_prc:
    Helper function to prune_functions. Inserts
    the hi_byte and low_byte to their positions
    in the program_counter

jmp_function:
    Iterates through jmp_ins objects to assign them to the
    program. If destination function does not exist, will
    "jump" to the current position in the program

app_functions:
    inserts the lo and hi bytes to the functions dict

app_prc:
    inserts the lo and hi bytes to the program_counter

find_func_pos:
    identifies where all function headers begin in
    the program - this solves the issue of how to exclude
    the position of the function header being physically in
    the program_counter list
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

    if(len(argv) > 2):
        print("Too many arguments")
        sys.exit(1)

    try:
        inputFile = argv[1]
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
        the binary file
    '''
    with open("a.out", "wb") as out:
        for func in functions:
            out.write(bytes(functions[func]))


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
    program_counter: list
        the list of functions and their
        opcodes/values

    Returns:
    -------------
    functions, program_counter after formatting
    for little endian
    '''
    for func in functions:
        for val in functions[func]:
            if val > 255:
                # get the low byte
                low_byte = val & 0b11111111
                # get the high byte
                hi_byte = val >> 8
                prune_func(functions[func],
                            low_byte, hi_byte, val)
                program_counter = prune_prc(program_counter, func,
                            low_byte, hi_byte, val)

    return functions, program_counter


def prune_func(func, low_byte, hi_byte, val):
    '''
    Helper function to prune_functions. Inserts
    the hi_byte and low_byte to their positions
    in the functions dict.

    Parameters:
    --------------
    func: list
        the list of the current function that needs
        a lower-endian format
    low_byte: int
        the lower byte of val
    hi_byte: int
        the high byte of val
    val:
        the value in question that we
        are splitting

    Returns:
    -------------
    func with the lower-endian format complete

    '''
    # determine which index that value is in the
    # functions dict
    index = func.index(val)
    # assign the low byte to val position
    func[index] = low_byte
    # insert the hi_byte after the low_byte
    # shift the rest of the list down
    func.insert((index+1), hi_byte)

    return func


def prune_prc(program_counter, func, low_byte, hi_byte, val):
    '''
    Helper function to prune_functions. Inserts
    the hi_byte and low_byte to their positions
    in the program_counter

    Parameters:
    --------------
    program_counter: list
        the list of the current program that needs
        a lower-endian format
    low_byte: int
        the lower byte of val
    hi_byte: int
        the high byte of val
    val:
        the value in question that we
        are splitting

    Returns:
    -------------
    program_counter with the lower-endian format complete

    '''
    # determine the index of the function
    ind_func = program_counter.index(func)
    # use that as a starting point to find the val index
    pro_ind = program_counter.index(val, ind_func)
    # at the former position of val, assign the low_byte
    program_counter[pro_ind] = low_byte
    # at the +1 position of low_byte, assign the hi_byte
    program_counter.insert((pro_ind+1), hi_byte)

    return program_counter


def jmp_function(functions, program_counter, jmp_list):
    '''
    Iterates through jmp_ins objects to assign them to the
    program. If destination function does not exist, will
    "jump" to the current position in the program

    Parameters:
    ----------------
    jmp_list: list
        list containing all jmp_ins objects
    functions: dict
        list of the opcodes/values in functions
    program_counter: list
        list of the opcodes/values in the program

    Returns:
    ----------------
    functions, program_counter after inserting the program_counter
    addresses of the jumps
    '''
    # if there were no jmp or jsr instructions, skip
    if len(jmp_list) == 0:
        return
    # iterate through the jmp_ins objects
    for jmp in jmp_list:
        # get the current position of each function header in the program
        func_pos = find_func_pos(program_counter)
        # determine the final destination in little endian
        jmp.dest_pos(func_pos[jmp.dest_name])
        # append the lo and hi bytes
        functions = app_functions(functions, jmp)
        # do the same for the program counter
        program_counter = app_prc(program_counter, jmp)

    return functions, program_counter


def app_functions(functions, jmp):
    '''
    inserts the lo and hi bytes to the functions dict

    Parameters:
    -------------
    functions: dict

    jmp: jmp_ins
        the particular jmp_ins we are inserting

    Returns:
    ------------
    functions after appending the jmp_ins
    '''
    # insert the low byte after the opcode
    functions[jmp.orig_name][jmp.lo_pos_func] = jmp.lo_byte
    # insert the high byte after the low byte
    functions[jmp.orig_name][jmp.hi_pos_func] = jmp.hi_byte

    return functions


def app_prc(program_counter, jmp):
    '''
    inserts the lo and hi bytes to the program_counter

    Parameters:
    -------------
    program_counter: list

    jmp: jmp_ins
        the particular jmp_ins we are inserting

    Returns:
    ------------
    program_counter after appending the jmp_ins
    '''

    # insert the lo byte
    program_counter[jmp.lo_pos_func + 1] = jmp.lo_byte
    # insert the hi byte
    program_counter[jmp.hi_pos_func + 1] = jmp.hi_byte

    return program_counter


def find_func_pos(program_counter):
    '''
    identifies where all function headers begin in
    the program - this solves the issue of how to exclude
    the position of the function header being physically in
    the program_counter list

    Parameters:
    -------------
    program_counter: list

    Returns:
    func_pos a dict of function_header: staring position
    '''
    func_pos = {}
    count = 0
    for x in program_counter:
        if isinstance(x, str):
            func_pos[x] = program_counter.index(x) - count
            count += 1

    return func_pos

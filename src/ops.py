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

swriter:
    Writes the data structures out to
    a .bin file that can be executed
    on the target processor
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
        TODO
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
                func = update_func(func,
                                low_byte, hi_byte, val)
                program_counter = update_prc(program_counter, func,
                                low_byte, hi_byte, val)

    return functions, program_counter


def update_func(func, low_byte, hi_byte, val):
    # determine which index that value is in the
    # functions dict
    index = func.index(val)
    # assign the low byte to val position
    func[index] = low_byte
    # insert the hi_byte after the low_byte
    # shift the rest of the list down
    func.insert((index+1), hi_byte)

    return func


def update_prc(program_counter, func, low_byte, hi_byte, val):
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

    Modifies:
    ----------------
    the functions dict and program counter to contain
    the assembly files jmp or jsr instructions
    '''
    # if there were no jmp or jsr instructions, skip
    if len(jmp_list) == 0:
        return
    # call prune_prc from ops.py to get correct jump positions
#    jmp_pos = prune_prc(program_counter)
    # iterate through the jmp_ins objects
    for jmp in jmp_list:
        # determine the final destination in little endian
        jmp.dest_pos()
        # append the lo and hi bytes
        functions = app_functions(functions, jmp)
        # do the same for the program counter
        program_counter = app_pc(program_counter, jmp)

    return functions, program_counter


def app_functions(functions, jmp):
    # insert the low byte after the opcode
    functions[jmp.orig_name][jmp.pos_func + 1] = jmp.lo_byte
    # insert the high byte after the low byte
    functions[jmp.orig_name][jmp.pos_func + 2] = jmp.hi_byte

    return functions


def app_pc(program_counter, jmp):
    # insert the lo byte
    program_counter[jmp.pos_counter + 1] = jmp.lo_byte
    # insert the hi byte
    program_counter[jmp.pos_counter + 2] = jmp.hi_byte

    return program_counter

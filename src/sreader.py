import re

"""
65py2 Reader
--------------------
A collection of functions for
processing 6502 Assembly files
into data structures

Methods:
--------------------

find_assignments:
    matches any variable assignments and 
    assigns them to a 

num_types:
    Identifies if a value is binary, hex, or decimal
    and returns the corresponding hexadecimal value

    num: must be between 0 and 255


find_functions:
    matches for a function name, iterates through function
    until a skipped line is discovered
    TODO nested functions
    returns a byte array of each function as one dictionary

"""

# Make some regular expressions for pattern matching
assignment = re.compile(r"(^[a-zA-Z0-9]+)\s?[=]\s?(\$[a-fA-F0-9]{2,4}|\%[0-1]{8}|[0-2]\d{2})")
assign = re.compile(r"^[a-zA-Z0-9]+")
num = re.compile(r"\$[a-fA-F0-9]{2,4}|\%[0-1]{8}|[0-2]\d{2}")
binary = re.compile(r"%[0-1]{8}")
hexadecimal = re.compile(r"$[a-fA-F0-9]{2,4}")
decimal = re.compile(r"[0-2]\d{2}")
function_header = re.compile("\w+\:")
command = re.compile(r"\t(\w+)\s(\$[a-fA-F0-9]{2,4}|\%[0-2]{8}|[0-2]\d{2})")
opcode = re.compile(r"\w{3}((\,\w\s)|\s)")
immediate = re.compile("#")

# Data Structures

# stores assignments in a dictionary
assignments = {}
# stores function names and indices to their contents in the list of bytearrays
function_headers = {}
# list containing bytearrays of functions
function_contents = []


def find_assignments(readFile):
    '''
    params
    outputs
    ''' 
    # iterate and assign to dictionary
    for line in readFile:
        if(re.match(assignment, line)):
            # get left name as string
            try:
                left = assign.findall(line)[0]
            except IndexError:
                continue
            # get right side
            try:
                right = num_type(num.findall(line)[0])
            except IndexError:
                continue
            assignments[left] = right
    return assignments

            
def num_type(line):
    '''
    param num
    returns hex num
    '''
    if re.match(r"%[0-1]{8}", line):
        # strip off %, make binary, then make hex
        return hex(int(line.lstrip('%'), 2))
    elif re.match(r"\$[a-fA-F0-9]{2,5}", line):
        return hex(int(line.lstrip('$'), 16)) 
    elif re.match(r"[0-2]\d{2}", line): 
        return hex(int(line)) 
    else:
        return -1


def function_reader(readFile, assignments, opcodes_list):
    func_num = 0
    func_bytearray = bytearray([])
    for line in readFile:
        if re.match(function_header, line):
            name = re.match(function_header, line)
            function_headers[name] = func_num
            func_num += 1
            while not ((re.match(r""), line) for line in readFile):
                if re.match(command, line):
                    return_bytearray = command_reader(line, assignments, opcodes_list)
                    func_bytearray += return_bytearray
                elif re.match(function_header, line):
                    pos = readFile.tell()
                    return_bytearray = function_reader(readFile.seek(pos, 0), assignments, opcodes_list)
                    func_bytearray += return_bytearray
                else:
                    continue
            function_contents[func_num] = func_bytearray
    return function_contents


def command_reader(line, assignments, opcodes_list):
    '''
    reading in left side for command TODO determine addressing
    access opcode_list and return hex of instruction
    reading in right side of line for assignment or 
    number return applicable hex
    returns a bytearray with applicable hex instructions
    '''
    try:
        left = opcode.findall(line)[0]
        if(re.search(immediate, line)):
           left = opcodes_list['imm'][left] 
    except IndexError:
        return
    try:
        right = num_type(num.findall(line)[0])
    except IndexError:
       right = assignments[left] 


#    def immediate(line):

'''coming soon
def indx(line):

def indy(line):
'''



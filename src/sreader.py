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

def find_assignments(readFile):
    '''
    params
    outputs
    '''
    #Make some regular expressions for pattern matching
    assignment = re.compile("(^[a-zA-Z0-9]+)\s?[=]\s?(\$[a-fA-F0-9]{2,4}|\%[0-1]{8}|[0-2]\d{2})")
    assign = re.compile("^[a-zA-Z0-9]+")
    num = re.compile("\$[a-fA-F0-9]{2,4}|\%[0-1]{8}|[0-2]\d{2}")
    assignments = {}
    
    #iterate and assign to dictionary
    for line in readFile:
        if(re.search(assignment, line)):
            #get left name as string
            try:
                left = assign.findall(line)[0]
            except IndexError:
                continue
            #get right side
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
   # binary = re.compile("%[0-1]{8}")
   # hexadecimal = re.compile("$[a-fA-F0-9]{2,4}")
   # decimal = re.compile("[0-2]\d{2}")

    if re.match("%[0-1]{8}", line):
        #strip off %, make binary, then make hex
        return hex(int(line.lstrip('%'), 2))
    elif re.match("\$[a-fA-F0-9]{2,5}", line):
        return hex(int(line.lstrip('$'), 16)) 
    elif re.match("[0-2]\d{2}", line): 
        return hex(int(line)) 
    else:
        return -1
'''       
#TODO
def function_reader(readFile, assignments, opcodes): 
    function_header = re.compile("\w+\:")
    command = re.compile("\t(\w+)\s(\$[a-fA-F0-9]{2,4}|\%[0-2]{8}|[0-2]\d{2}))


'''


#    def immediate(line):

'''coming soon
def indx(line):

def indy(line):
'''




    



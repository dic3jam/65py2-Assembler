# from src.sreader import program_counter


class jmp_ins:
    '''
    Class: jmp_ins

    A container for holding all relevant information
    for 65py2 to add jmp or jsr commands to
    the binary file

    Attributes:
    ---------------
    orig_name: str
        the name of the function that called a jmp or
        jsr instruction
    lo_pos_func: integer
        the position the low byte will sit after the call
        to dest_pos
    hi_pos_func: integer
        the position the high byte will sit after the call
        to dest_pos
    dest_name: str
        the function header that was called for for the jmp
        or jsr instruction
    lo_byte: integer
        created by the create_jmp method after being called in
        sreader.jmp_function. Processes the dest_name for a program
        counter position holds the low byte of that destination
    hi_byte: integer
        created by the create_jmp method after being called in
        sreader.jmp_function. Processes the dest_name for a program
        counter position holds the high byte of that destination

    Methods:
    -------------
    dest_pos: 
        receives the final program counter position and
        assigns the lo_byte and hi_byte of that position to
        this
        
        Parameters:
        --------------
        jmp_pos: int
            the position of the jmp destination function
            as determined by sreader.find_func_pos

    '''

    def __init__(self, orig_name, lo_pos_func, hi_pos_func, dest_name):
        self.orig_name = orig_name
        self.lo_pos_func = lo_pos_func
        self.hi_pos_func = hi_pos_func
        self.dest_name = dest_name
        self.lo_byte = 0xEA
        self.hi_byte = 0xEA

    def dest_pos(self, jmp_pos):
        self.lo_byte = jmp_pos & 0b11111111
        self.hi_byte = jmp_pos >> 8

   

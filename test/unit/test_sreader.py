from src.sreader import *
import unittest


class Testsreader(unittest.Testcase):

    # def setup():

    def test_find_assignments(self, readFile):

    def test_num_type(self, line):

    def test_jmp_function(self, fnc_header):

    def test_jsr_function(self, fnc_header):

    def test_function_reader(self, readFile, assignments, opcodes_list):

    def test_command_reader(self, line, opcodes_list):


    def test_inc_counter(self, symbol):


    if __name__ == '__main__':
        unittest.main()

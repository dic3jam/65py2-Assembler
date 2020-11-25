from src.sreader import *
from src.jmp_ins import jmp_ins
from src.ops import *
import unittest
import pdb

class test_find_assignments(unittest.TestCase):

    def test_finds_variables(self):
        readFile = open("test/check_variables.s", "r")
        assign = find_assignments(readFile)
        self.assertEqual(assign["variable1"], 5)
        self.assertEqual(assign["VARIABLEA"], 2)
        self.assertEqual(assign["check"], 42)
        self.assertEqual(assign["thishexwillwork"], 0x42)
        self.assertEqual(assign["thisbinwillwork"], 0b01010010)
        readFile.close()


class test_num_types(unittest.TestCase):


    def setUp(self):
        self.variables = {"variable5": 42, "variable6": 0x42}

    def test_numover_FFFF(self):
        tooMuch = "$FFFFFFFF"
        yaNo = num_type(tooMuch, self.variables)
        self.assertEqual(yaNo, 234)

    def test_looksup_variable(self):
        # pdb.set_trace()
        fourtytwo = "\tlda variable5"
        itsfourtytwo = num_type(fourtytwo, self.variables)
        self.assertEqual(itsfourtytwo, 42)

    def test_returns_function_header(self):
        header_line = "\tjsr func_header"
        funcheader = num_type(header_line, self.variables)
        self.assertEqual(funcheader, "func_header")


class test_jmp_function(unittest.TestCase):

    def setUp(self):
        functions = {"main": [0xad, 0x42, 0x8d, 0xdd, 0x4c, 0x00,
                            0x00, 0x4c, 0x00, 0x00], "jmp_here": [0x4c, 0x00, 0x00]}
        program_counter = ["main", 0xad, 0x42, 0x8d, 0xdd, 0x4c, 0x00, 0x00, 0x4c, 0x00, 0x00,
                        "jmp_here", 0x4c, 0x00, 0x00]
        jmp_list = []
        jmp_list.append(jmp_ins("main", 5, 4, "jmp_here"))
        jmp_list.append(jmp_ins("main", 8, 7, "jmp_here"))
        jmp_list.append(jmp_ins("jmp_here", 12, 11, "jmp_here"))

    def test_jmp(self):
        jmp_function()
        check_counter = ["main", 0xad, 0x42, 0x8d, 0xdd, 0x4c, 0x0A, 0x00, 0x4c, 0x0A, 0x00,
                            "jmp_here", 0x4c, 0x0A, 0x00]
        for x in range(len(program_counter)):
            self.assertEqual(check_counter[x], program_counter[x])


class test_function_reader(unittest.TestCase):

    def test_untilithinkofsomething(self):
        self.assertEqual(1, 1)


class test_command_reader(unittest.TestCase):

    def test_read_acc(self):
        line = "\trol"
        com = command_reader(line, opcodes_list)
        self.assertEqual(0x2a, com)

    def test_read_imm(self):
        line = "\tsbc #42"
        com = command_reader(line, opcodes_list)
        self.assertEqual(0xe9, com)

    def test_read_abso(self):
        line = "\tinc 42"
        com = command_reader(line, opcodes_list)
        self.assertEqual(0xee, com)

    def test_read_imp(self):
        line = "\tpha"
        com = command_reader(line, opcodes_list)
        self.assertEqual(0x48, com)

    def test_read_rel(self):
        line = "\tbcc"
        com = command_reader(line, opcodes_list)
        self.assertEqual(0x90, com)


class test_prune_functions(unittest.TestCase):

    def test_prune_functions(self):
        functions = {"main": [0xAAAA, 0xFFFF, 0xBBBB]}
        program_counter = ["main", 0xAAAA, 0xFFFF, 0xBBBB]
        prune_functions(functions, program_counter)
        self.assertEqual(functions["main"][1], 0xAA)
        self.assertEqual(functions["main"][5], 0xBB)
        self.assertEqual(program_counter[1], 0xAA)
        self.assertEqual(program_counter[3], 0xFF)


if __name__ == '__main__':
    unittest.main()

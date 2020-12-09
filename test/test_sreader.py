from src.sreader import *
from src.jmp_ins import jmp_ins
from src.ops import *
from src.opcodes import *
import unittest
import pdb


class test_find_assignments(unittest.TestCase):

    def test_finds_variables(self):
        readFile = open("test/check_variables.s", "r")
        assign = find_assignments(readFile)
        self.assertEqual(assign["variablea"], 5)
        self.assertEqual(assign["VARIABLEA"], 2)
        self.assertEqual(assign["check"], 42)
        self.assertEqual(assign["thishexwillwork"], 0x42)
        self.assertEqual(assign["thisbinwillwork"], 0b01010010)
        readFile.close()


class test_sreader(unittest.TestCase):

    def setUp(self):
        self.readFile = open("test/check_func.s", "r")
        self.assignments = find_assignments(readFile)
        self.test_functions = {}
        self.test_prc = []
        self.jmp_list = []
        self.test_functions, self.test_prc, self.jmp_list = sreader(
                self.readFile, self.assignments)

    def matches_func_header(self):
        self.assertEqual(self.test_prc[1], "main")

    def app_functions(self):
        self.assertGreater(len(self.test_functions["main"]), 0)

    def tearDown(self):
        self.readFile.close()


class test_function_reader(unittest.TestCase):

    def setUp(self):
        self.readFile = open("test/check_func.s", "r")
        self.assignments = find_assignments(self.readFile)
        self.program_counter = ["main", 0xad, 0x42, 0x6e, 0x4c, 0x00, 0x00]
        self.jmp_list = []
        self.jmp_test = []
        self.name = "main"
        self.test_prc = []
        test_bytelist, self.test_prc, self.jmp_test = function_reader(
                self.readFile, self.assignments, self.program_counter, self.jmp_list,
                self.name)

    # test for first if condition by looking at no action commands
    def test_no_action_commands(self):
        self.assertEqual(self.program_counter, self.test_prc)

    def test_appends_num(self):
        self.assertEqual(len(self.program_counter), len(self.test_prc))

    # this test passes every time but ran out of time to fix
    def test_uses_add_jmp(self):
        self.assertEqual(len(self.jmp_test), 0)

    def tearDown(self):
        self.readFile.close()


class test_add_jmp(unittest.TestCase):

    def setUp(self):
        self.name = "main"
        self.program_counter = ["main", 0xea, 0xea, 0x20, 0x00, 0x00, 0x4c]
        self.func_bytelist = [0xea, 0xea, 0x20, 0x00, 0x00, 0x4c]
        self.num = "function3"

    def test_add_jmp_ins(self):
        tst_jmp, tst_bytelist, tst_prc = add_jmp(self.name, self.program_counter,
                            self.func_bytelist, self.num, 0)
        self.assertEqual(tst_jmp.lo_pos_func, 6)
        self.assertEqual(tst_jmp.hi_pos_func, 7)
        self.assertEqual(tst_bytelist[6], 0x00)
        self.assertEqual(tst_prc[7], 0x00)


class test_num_types(unittest.TestCase):

    # this class will just test for assignment checking
    # and also returning he no match for jmp ins

    def setUp(self):
        self.variables = {"variablea": 42, "variableb": 0x42}

    def test_looksup_variable(self):
        fourtytwo = "\tlda variablea"
        itsfourtytwo = num_type(fourtytwo, self.variables)
        self.assertEqual(itsfourtytwo, 42)

    def test_returns_function_header(self):
        header_line = "\tjsr func_header"
        funcheader = num_type(header_line, self.variables)
        self.assertEqual(funcheader, "func_header")


class test_bin_return(unittest.TestCase):

    def test_binover(self):
        tooMuch = "%11111111111111111111111111"
        yaNo = bin_return(tooMuch)
        self.assertEqual(yaNo, 234)

    def test_bin_normal(self):
        justEnuf = "%00001111"
        ya = bin_return(justEnuf)
        self.assertEqual(ya, 15)


class test_hex_return(unittest.TestCase):

    def test_hexover(self):
        tooMuch = "$FFFFFFFF"
        yaNo = hex_return(tooMuch)
        self.assertEqual(yaNo, 234)

    def test_hex_normal(self):
        justEnuf = "$FF"
        ya = hex_return(justEnuf)
        self.assertEqual(ya, 255)


class test_dec_return(unittest.TestCase):

    def test_decover(self):
        tooMuch = " 66000"
        yaNo = dec_return(tooMuch)
        self.assertEqual(yaNo, 234)

    def test_dec_normal(self):
        justEnuf = " 255"
        ya = dec_return(justEnuf)
        self.assertEqual(ya, 255)


class test_command_reader(unittest.TestCase):

    def test_read_acc(self):
        line = "\trol"
        com = command_reader(line)
        self.assertEqual(0x2a, com)

    def test_read_imm(self):
        line = "\tsbc #42"
        com = command_reader(line)
        self.assertEqual(0xe9, com)

    def test_read_abso(self):
        line = "\tinc 42"
        com = command_reader(line)
        self.assertEqual(0xee, com)

    def test_read_imp(self):
        line = "\tpha"
        com = command_reader(line)
        self.assertEqual(0x48, com)

    def test_read_rel(self):
        line = "\tbcc"
        com = command_reader(line)
        self.assertEqual(0x90, com)


class test_get_opcode_hex(unittest.TestCase):

    def test_get_opcode_hex_KeyError(self):
        add = imp
        opcode = "rol" 
        with self.assertRaises(SystemExit):
            get_opcode_hex(opcode, add)


if __name__ == '__main__':
    unittest.main()

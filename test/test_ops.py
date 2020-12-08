import io
import unittest
from src.jmp_ins import *
from src.ops import *
from src.opcodes import *


class test_checkThenOpen(unittest.TestCase):

    def setUp(self):
        self.argv = []
        self.argv.append("main.py")

    # test above and below boundry for number of args in sys.argv
    def test_argv_1(self):
        with self.assertRaises(SystemExit):
            checkThenOpen(self.argv)

    def test_argv_3(self):
        self.argv.append("two")
        self.argv.append("three")
        with self.assertRaises(SystemExit):
            checkThenOpen(self.argv)

    # test for presence of an input file, and that that file exists

    def test_inputFile_fail(self):
        self.argv.append("not_found.s")
        with self.assertRaises(FileNotFoundError):
            checkThenOpen(self.argv)

    def test_opens_file(self):
        self.argv.append("test/check_variables.s")
        readFile = checkThenOpen(self.argv)
        self.assertIs(type(readFile), io.TextIOWrapper)
        readFile.close()


class test_swriter(unittest.TestCase):

    def test_swriter_output(self):
        functions = {"main": [0xEA, 0xEA, 0xEA, 0xEA]}
        swriter(functions)
        checkFile = open("a.out", "rb")
        checkEA = list(checkFile.read())
        itWorks = True
        for x in checkEA:
            if x != 0xEA:
                itWorks = False
                break
        self.assertTrue(itWorks)
        checkFile.close()


class test_prune_functions(unittest.TestCase):

    def test_prune_functions(self):
        functions = {"main": [0xAAAA, 0xFFFF, 0xBBBB]}
        program_counter = ["main", 0xAAAA, 0xFFFF, 0xBBBB]
        prune_functions(functions, program_counter)
        self.assertEqual(functions["main"][1], 0xAA)
        self.assertEqual(functions["main"][5], 0xBB)
        self.assertEqual(program_counter[1], 0xAA)
        self.assertEqual(program_counter[3], 0xFF)


class test_update_func(unittest.TestCase):

    def test_adds_jmp_func(self):
        func = ["main", 0xea, 0xea, 0x4c]
        lo = 0x42
        hi = 0x42
        val = 3
        test_func = update_func(func, lo, hi, val)
        self.assertEqual(test_func[4], 0x42)
        self.assertEqual(test_func[5], 0x42)


class test_update_prc(unittest.TestCase):

    def test_adds_jmp_prc(self):
        func = {"main": [0xea, 0xea, 0x4c]}
        prc = ["main", 0xea, 0xea, 0x4c]
        lo = 0x42
        hi = 0x42
        val = 3
        test_func = update_prc(prc, func, lo, hi, val)
        self.assertEqual(test_func[4], 0x42)
        self.ssertEqual(test_func[5], 0x42)


class test_jmp_function(unittest.TestCase):

    def setUp(self):
        self.functions = {"main": [0xad, 0x42, 0x8d, 0xdd, 0x4c, 0x00,
                            0x00, 0x4c, 0x00, 0x00], "jmp_here": [0x4c, 0x00, 0x00]}
        self.program_counter = ["main", 0xad, 0x42, 0x8d, 0xdd, 0x4c, 0x00, 0x00, 0x4c, 0x00, 0x00,
                        "jmp_here", 0x4c, 0x00, 0x00]
        self.jmp_list = []
        self.jmp_list.append(jmp_ins("main", 5, 4, "jmp_here"))
        self.jmp_list.append(jmp_ins("main", 8, 7, "jmp_here"))
        self.jmp_list.append(jmp_ins("jmp_here", 12, 11, "jmp_here"))

    def test_jmp(self):
        test_functions = {}
        test_prc = []
        test_functions, test_prc = jmp_function(self.functions, self.program_counter,
                self.jmp_list)
        check_counter = ["main", 0xad, 0x42, 0x8d, 0xdd, 0x4c, 0x0A, 0x00, 0x4c, 0x0A, 0x00,
                            "jmp_here", 0x4c, 0x0A, 0x00]
        for x in range(len(program_counter)):
            self.assertEqual(check_counter[x], program_counter[x])


'''
class test_app_functions(unittest.TestCase):

    # TODO


class test_app_prc(unittest.TestCase):

    # TODO
'''


if __name__ == '__main__':
    unittest.main()

import io
import unittest

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


class test_get_opcode_hex(unittest.TestCase):

    def test_get_opcode_hex_KeyError(self):
        add = imp
        opcode = "rol" 
        with self.assertRaises(SystemExit):
            get_opcode_hex(opcode, add)


class test_swriter(unittest.TestCase):

    def test_swriter_output(self):
        functions = {"main":[0xEA, 0xEA, 0xEA, 0xEA]} 
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


if __name__ == '__main__':
    unittest.main()

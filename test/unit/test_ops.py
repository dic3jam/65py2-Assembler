import sys
import unittest

from src.ops import *


class test_checkThenOpen(unittest.TestCase):

    def setUp(self):
        argv = []
        argv.append(main)

    def test_argv_1(self):
        checkThenOpen(argv)
        self.assertEqual(sys.exit, 1)

    def test_argv_2(self):
        argv.append(two)
        checkThenOpen(argv)
        self.assertEqual(sys.exit, 0)





if __name__ == '__main__':
    unittest.main()

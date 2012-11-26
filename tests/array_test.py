import unittest

from array import Array, ArrayError


class ArrayTest(unittest.TestCase):

    def test_init(self):
        a = Array(5, 3, 0)

        self.assertEqual(a._width, 15)
        self.assertEqual(a._height, 10)
        self.assertEqual(a._empty, 0)

        self.assertEqual(
            a._array,
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
        )

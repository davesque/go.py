import unittest

from go.array import Array, ArrayError


class ArrayTest(unittest.TestCase):

    def test_init(self):
        a = Array(5, 3, 0)

        self.assertEqual(a._width, 5)
        self.assertEqual(a._height, 3)
        self.assertEqual(a._empty, 0)

        self.assertEqual(
            a._array,
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
        )

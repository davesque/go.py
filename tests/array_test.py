import unittest

from go.array import Array, ArrayError


class ArrayTest(unittest.TestCase):

    def test_init(self):
        a = Array(4, 3, 0)

        self.assertEqual(a._width, 4)
        self.assertEqual(a._height, 3)
        self.assertEqual(a._empty, 0)

        self.assertEqual(
            a._array,
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ],
        )

    def test_get_or_set_index(self):
        a = Array(4, 3, 0)

        a[(1, 1)] = 1
        a[(3, 1)] = 2

        self.assertEqual(
            a._array,
            [
                [1, 0, 2, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ],
        )

        self.assertEqual(a[(1, 1)], 1)
        self.assertEqual(a[(2, 1)], 0)

    def test_get_or_set_invalid_index(self):
        a = Array(4, 3, 0)

        self.assertRaises(ArrayError, a.__getitem__, (10, 10))
        self.assertRaises(ArrayError, a.__setitem__, (10, 10), 10)

    def test_equality(self):
        a1 = Array(4, 3, 0)
        a2 = Array(4, 3, 0)
        a3 = Array(4, 3, 0)

        a1[(1, 1)] = 1
        a2[(1, 1)] = 1

        self.assertEqual(a1, a2)
        self.assertNotEqual(a1, a3)

        a4 = Array(5, 5)
        a5 = Array(12, 34)

        self.assertNotEqual(a4, a5)

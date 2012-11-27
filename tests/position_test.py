import unittest

from go import Position, PositionError


class PositionTest(unittest.TestCase):

    def setUp(self):
        self.p1 = Position('black')
        self.p2 = Position('white')
        self.p3 = Position('empty')
        self.p4 = Position('black')

    def test_init_with_valid_type(self):
        self.assertEqual(self.p1._type, 'black')
        self.assertEqual(self.p2._type, 'white')
        self.assertEqual(self.p3._type, 'empty')

    def test_init_with_invalid_type(self):
        self.assertRaises(PositionError, Position, 'arst')

    def test_equality(self):
        self.assertEqual(self.p1, self.p4)
        self.assertNotEqual(self.p2, self.p4)

    def test_str(self):
        self.assertEqual(str(self.p1), '\x1b[1m@\x1b[0m')
        self.assertEqual(str(self.p2), '\x1b[1mO\x1b[0m')
        self.assertEqual(str(self.p3), '.')

    def test_repr(self):
        self.assertEqual(repr(self.p1), 'Black')
        self.assertEqual(repr(self.p2), 'White')
        self.assertEqual(repr(self.p3), 'Empty')

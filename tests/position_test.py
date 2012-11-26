import unittest

from position import Position, PositionError


class PositionTest(unittest.TestCase):

    def test_init_with_valid_type(self):
        p1 = Position('black')
        p2 = Position('white')
        p3 = Position('empty')

        self.assertEqual(p1._type, 'black')
        self.assertEqual(p2._type, 'white')
        self.assertEqual(p3._type, 'empty')

    def test_init_with_invalid_type(self):
        self.assertRaises(PositionError, Position, 'arst')

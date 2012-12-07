import unittest

from go import Location, LocationError


class LocationTest(unittest.TestCase):

    def setUp(self):
        self.l1 = Location('black')
        self.l2 = Location('white')
        self.l3 = Location('empty')
        self.l4 = Location('black')

    def test_init_with_valid_type(self):
        self.assertEqual(self.l1._type, 'black')
        self.assertEqual(self.l2._type, 'white')
        self.assertEqual(self.l3._type, 'empty')

    def test_init_with_invalid_type(self):
        self.assertRaises(LocationError, Location, 'arst')

    def test_equality(self):
        self.assertEqual(self.l1, self.l4)
        self.assertNotEqual(self.l2, self.l4)

    def test_str(self):
        self.assertEqual(str(self.l1), '\x1b[1m@\x1b[0m')
        self.assertEqual(str(self.l2), '\x1b[1mO\x1b[0m')
        self.assertEqual(str(self.l3), '.')

    def test_repr(self):
        self.assertEqual(repr(self.l1), 'Black')
        self.assertEqual(repr(self.l2), 'White')
        self.assertEqual(repr(self.l3), 'Empty')

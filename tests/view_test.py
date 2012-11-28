import unittest

from go import Board, View


class ViewTest(unittest.TestCase):

    def setUp(self):
        self.b = Board(9)
        self.v = View(self.b)

    def test_init(self):
        self.assertEqual(self.v._board, self.b)
        self.assertEqual(self.v._cursor, (1, 1))

        self.assertEqual(self.v._hoshis, (
            (3, 3), (7, 3), (3, 7), (7, 7), (5, 5),
        ))

        e = str(Board.EMPTY)
        h = View.HOSHI

        self.assertEqual(self.v._array, [
            [e, e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e, e],
            [e, e, h, e, e, e, h, e, e],
            [e, e, e, e, e, e, e, e, e],
            [e, e, e, e, h, e, e, e, e],
            [e, e, e, e, e, e, e, e, e],
            [e, e, h, e, e, e, h, e, e],
            [e, e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e, e],
        ])

    def test_get_hoshis(self):
        self.assertEqual(self.v._get_hoshis(19), (
            (4, 4), (16, 4), (4, 16), (16, 16),
            (10, 10),
            (4, 10), (10, 4), (16, 10), (10, 16),
        ))

        self.assertEqual(self.v._get_hoshis(18), (
            (4, 4), (15, 4), (4, 15), (15, 15),
        ))

        self.assertEqual(self.v._get_hoshis(13), (
            (4, 4), (10, 4), (4, 10), (10, 10),
            (7, 7),
        ))

    def test_in_width(self):
        self.assertEqual(self.v._in_width(100), 9)
        self.assertEqual(self.v._in_width(-123), 1)
        self.assertEqual(self.v._in_width(3), 3)

    def test_in_height(self):
        self.assertEqual(self.v._in_height(100), 9)
        self.assertEqual(self.v._in_height(-123), 1)
        self.assertEqual(self.v._in_height(3), 3)

    def test_cursor_movement(self):
        self.assertEqual(self.v.cursor, (1, 1))

        self.v.cursor_up()
        self.v.cursor_left()

        self.assertEqual(self.v.cursor, (1, 1))

        self.v.cursor_right()
        self.v.cursor_right()
        self.v.cursor_down()

        self.assertEqual(self.v.cursor, (3, 2))

        self.v.cursor_up()
        self.v.cursor_left()
        self.v.cursor_down()
        self.v.cursor_down()
        self.v.cursor_down()

        self.assertEqual(self.v.cursor, (2, 4))

        for i in range(12):
            self.v.cursor_right()
            self.v.cursor_down()

        self.assertEqual(self.v.cursor, (9, 9))

    def test_str(self):
        self.assertEqual(
            str(self.v),
            'X . . . . . . . .\n'
            '. . . . . . . . .\n'
            '. . + . . . + . .\n'
            '. . . . . . . . .\n'
            '. . . . + . . . .\n'
            '. . . . . . . . .\n'
            '. . + . . . + . .\n'
            '. . . . . . . . .\n'
            '. . . . . . . . .'
        )

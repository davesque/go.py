import unittest

from go import Board, BoardError


class BoardTest(unittest.TestCase):
    """
    Won't test any of the array functionality.  That is covered in
    array_test.py.
    """

    def setUp(self):
        self.bo = Board(5)

    @classmethod
    def get_test_board_1(cls):
        _ = Board.EMPTY
        B = Board.BLACK
        W = Board.WHITE

        bo = Board(19)

        bo._array = [
            [B, B, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, W, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, W, _, W, B, W, _, B, _, _, _, _, _, _, _, _, _, _, _],
            [_, W, _, _, W, _, _, B, B, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, W, W, W, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, B, B, W, _, W, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, B, B, W, W, W, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, W, W, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, B, B, B, W, W, W, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, B, _, B, W, _, W, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, B, B, B, W, _, W, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, B, B, W, W, _, W, W, _, _],
            [_, _, _, _, _, _, _, _, _, _, B, B, B, B, B, W, _, W, _],
            [_, _, _, _, _, _, _, _, _, _, B, _, B, B, B, W, W, _, _],
            [_, _, _, _, _, _, _, _, _, _, B, _, B, B, W, W, W, _, _],
        ]

        return bo, _, B, W

    def test_init(self):
        e = Board.EMPTY
        b = Board.BLACK
        w = Board.WHITE

        self.assertEqual(self.bo._array, [
            [e, e, e, e, e],
            [e, e, e, e, e],
            [e, e, e, e, e],
            [e, e, e, e, e],
            [e, e, e, e, e],
        ])

        self.assertTrue(self.bo._turn is b)
        self.assertEqual(self.bo._score, {b: 0, w: 0})
        self.assertEqual(self.bo._history, [])
        self.assertEqual(self.bo._redo, [])

    def test_turn(self):
        self.assertEqual(self.bo.turn, 'Black')
        self.bo.move(1, 1)
        self.assertEqual(self.bo.turn, 'White')
        self.bo.move(2, 2)
        self.assertEqual(self.bo.turn, 'Black')
        self.bo.move(3, 3)
        self.assertEqual(self.bo.turn, 'White')

    def test_score(self):
        e = Board.EMPTY
        b = Board.BLACK
        w = Board.WHITE

        self.assertEqual(self.bo.score, {
            'black': 0,
            'white': 0,
        })

        self.bo._array = [
            [w, b, e, e, e],
            [e, e, e, e, e],
            [e, e, e, e, e],
            [e, e, e, e, e],
            [e, e, e, e, e],
        ]
        self.bo.move(1, 2)

        self.assertEqual(self.bo.score, {
            'black': 1,
            'white': 0,
        })

        self.setUp()
        self.bo._array = [
            [w, b, e, e, e],
            [w, b, e, e, e],
            [e, w, b, e, e],
            [w, b, e, e, e],
            [b, e, e, e, e],
        ]
        self.bo.move(1, 3)

        self.assertEqual(self.bo.score, {
            'black': 4,
            'white': 0,
        })

    def test_next_turn(self):
        b = Board.BLACK
        w = Board.WHITE

        self.assertTrue(self.bo._next_turn is w)
        self.bo.move(1, 1)
        self.assertTrue(self.bo._next_turn is b)
        self.bo.move(2, 2)
        self.assertTrue(self.bo._next_turn is w)
        self.bo.move(3, 3)
        self.assertTrue(self.bo._next_turn is b)

    def test_flip_turn(self):
        b = Board.BLACK
        w = Board.WHITE

        self.assertEqual(self.bo._turn, b)
        self.bo._flip_turn()
        self.assertEqual(self.bo._turn, w)
        self.bo._flip_turn()
        self.assertEqual(self.bo._turn, b)
        self.bo._flip_turn()
        self.assertEqual(self.bo._turn, w)

    def test_state(self):
        e = Board.EMPTY
        b = Board.BLACK
        w = Board.WHITE

        state = (
            [
                [e, e, e, e, e],
                [e, e, e, e, e],
                [e, e, e, e, e],
                [e, e, e, e, e],
                [e, e, e, e, e],
            ],
            b,
            {
                b: 0,
                w: 0,
            },
        )
        _state = self.bo._state

        self.assertEqual(_state[0], state[0])
        self.assertEqual(_state[1], state[1])
        self.assertEqual(_state[2], state[2])

        self.assertTrue(_state[0] is not state[0])
        self.assertTrue(_state[1] is state[1])
        self.assertTrue(_state[2] is not state[2])

        self.bo.move(3, 3)

        state = (
            [
                [e, e, e, e, e],
                [e, e, e, e, e],
                [e, e, b, e, e],
                [e, e, e, e, e],
                [e, e, e, e, e],
            ],
            w,
            {
                b: 0,
                w: 0,
            },
        )
        _state = self.bo._state

        self.assertEqual(_state[0], state[0])
        self.assertEqual(_state[1], state[1])
        self.assertEqual(_state[2], state[2])

        self.assertTrue(_state[0] is not state[0])
        self.assertTrue(_state[1] is state[1])
        self.assertTrue(_state[2] is not state[2])

    def test_load_state(self):
        state = self.bo._state

        self.bo.move(3, 3)

        self.assertNotEqual(self.bo._state, state)

        self.bo._load_state(state)

        self.assertEqual(self.bo._state, state)

    def test_push_history(self):
        self.assertEqual(self.bo._history, [])

        state = self.bo._state

        self.bo._push_history()

        self.assertTrue(len(self.bo._history) == 1)
        self.assertEqual(self.bo._history[0], state)

    def test_pop_history(self):
        self.assertEqual(self.bo._history, [])

        state = self.bo._state
        self.bo.move(3, 3)

        self.assertNotEqual(self.bo._state, state)

        self.bo._pop_history()

        self.assertEqual(self.bo._state, state)

    def test_undo(self):
        self.assertRaises(BoardError, self.bo.undo)
        self.assertEqual(self.bo._redo, [])
        self.assertEqual(self.bo._history, [])

        state1 = self.bo._state
        self.bo.move(3, 3)

        self.assertNotEqual(self.bo._state, state1)
        self.assertEqual(self.bo._history, [state1])
        self.assertEqual(self.bo._redo, [])

        state2 = self.bo._state
        pop_state = self.bo.undo()

        self.assertEqual(self.bo._state, state1)
        self.assertEqual(pop_state, state2)
        self.assertNotEqual(self.bo._state, pop_state)

        self.assertEqual(self.bo._history, [])
        self.assertEqual(self.bo._redo, [pop_state])

    def test_redo(self):
        self.assertRaises(BoardError, self.bo.undo)
        self.assertEqual(self.bo._redo, [])
        self.assertEqual(self.bo._history, [])

        state1 = self.bo._state
        self.bo.move(3, 3)

        self.assertNotEqual(self.bo._state, state1)
        self.assertEqual(self.bo._history, [state1])
        self.assertEqual(self.bo._redo, [])

        state2 = self.bo._state
        pop_state = self.bo.undo()

        self.assertEqual(self.bo._state, state1)
        self.assertEqual(pop_state, state2)
        self.assertNotEqual(self.bo._state, pop_state)

        self.assertEqual(self.bo._history, [])
        self.assertEqual(self.bo._redo, [pop_state])

        self.bo.redo()

        self.assertEqual(self.bo._state, state2)
        self.assertNotEqual(self.bo._state, state1)
        self.assertEqual(self.bo._history, [state1])
        self.assertEqual(self.bo._redo, [])

    def test_tally(self):
        self.assertEqual(self.bo.score, {
            'black': 0,
            'white': 0,
        })

        self.bo._tally(100)

        self.assertEqual(self.bo.score, {
            'black': 100,
            'white': 0,
        })

        self.bo.move(3, 3)
        self.bo._tally(100)

        self.assertEqual(self.bo.score, {
            'black': 100,
            'white': 100,
        })

    def test_get_none(self):
        e = Board.EMPTY
        b = Board.BLACK
        w = Board.WHITE

        self.assertTrue(self.bo._get_none(1, 1) is e)
        self.bo.move(3, 3)
        self.assertTrue(self.bo._get_none(3, 3) is b)
        self.bo.move(3, 2)
        self.assertTrue(self.bo._get_none(3, 2) is w)
        self.assertTrue(self.bo._get_none(-1, 100) is None)

    def test_get_surrounding(self):
        e = Board.EMPTY
        b = Board.BLACK
        w = Board.WHITE

        self.assertEqual(self.bo._get_surrounding(3, 3), [
            (e, (3, 2)),
            (e, (4, 3)),
            (e, (3, 4)),
            (e, (2, 3)),
        ])

        self.bo.move(1, 1)

        self.assertEqual(self.bo._get_surrounding(2, 1), [
            (e, (3, 1)),
            (e, (2, 2)),
            (b, (1, 1)),
        ])

        self.bo.move(2, 1)

        self.assertEqual(self.bo._get_surrounding(1, 1), [
            (w, (2, 1)),
            (e, (1, 2)),
        ])
        self.assertEqual(self.bo._get_surrounding(5, 5), [
            (e, (5, 4)),
            (e, (4, 5)),
        ])

    def test_get_group(self):
        bo = self.get_test_board_1()[0]

        # Assert only black of white group is fetched
        self.assertRaises(BoardError, bo.get_group, 3, 1)
        self.assertRaises(BoardError, bo.get_group, 10, 10)

        # Assert correct upper-left groups
        self.assertEqual(bo.get_group(1, 1), set([
            (1, 1), (2, 1),
        ]))
        self.assertEqual(bo.get_group(2, 1), set([
            (1, 1), (2, 1),
        ]))
        self.assertEqual(bo.get_group(2, 3), set([
            (2, 3), (2, 4),
        ]))
        self.assertEqual(bo.get_group(5, 2), set([
            (5, 2),
        ]))
        self.assertEqual(bo.get_group(5, 3), set([
            (5, 3),
        ]))
        self.assertEqual(bo.get_group(8, 3), set([
            (8, 3), (8, 4), (9, 4),
        ]))
        self.assertEqual(bo.get_group(2, 7), set([
            (2, 7), (3, 7), (2, 8), (3, 8),
        ]))
        self.assertEqual(bo.get_group(2, 6), set([
            (2, 6), (3, 6), (4, 6), (4, 7),
            (4, 8), (4, 9), (3, 9), (5, 8),
            (6, 8), (6, 7),
        ]))

        # Assert correct lower-right groups
        self.assertEqual(bo.get_group(11, 13), set([
            (11, 13), (11, 14), (11, 15), (11, 16),
            (11, 17), (11, 18), (11, 19), (12, 13),
            (12, 15), (12, 16), (12, 17), (13, 13),
            (13, 14), (13, 15), (13, 17), (13, 18),
            (13, 19), (14, 17), (14, 18), (14, 19),
            (15, 17), (15, 18),
        ]))
        self.assertEqual(bo.get_group(14, 13), set([
            (13, 16), (14, 13), (14, 14), (14, 15),
            (14, 16), (15, 13), (15, 19), (16, 13),
            (16, 14), (16, 15), (16, 16), (16, 17),
            (16, 18), (16, 19), (17, 16), (17, 18),
            (17, 19),
        ]))

    def test_kill_group(self):
        bo, _, B, W = self.get_test_board_1()

        # Assert only black of white group is fetched
        self.assertRaises(BoardError, bo._kill_group, 3, 1)
        self.assertRaises(BoardError, bo._kill_group, 10, 10)

        # Assert correct upper-left groups
        self.assertEqual(bo._kill_group(1, 1), 2)
        self.assertEqual(bo._kill_group(2, 3), 2)
        self.assertEqual(bo._kill_group(5, 2), 1)
        self.assertEqual(bo._kill_group(5, 3), 1)
        self.assertEqual(bo._kill_group(8, 3), 3)
        self.assertEqual(bo._kill_group(2, 7), 4)
        self.assertEqual(bo._kill_group(2, 6), 10)
        self.assertEqual(bo._array, [
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, W, _, W, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, W, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, B, B, B, W, W, W, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, B, _, B, W, _, W, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, B, B, B, W, _, W, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, B, B, W, W, _, W, W, _, _],
            [_, _, _, _, _, _, _, _, _, _, B, B, B, B, B, W, _, W, _],
            [_, _, _, _, _, _, _, _, _, _, B, _, B, B, B, W, W, _, _],
            [_, _, _, _, _, _, _, _, _, _, B, _, B, B, W, W, W, _, _],
        ])

        # Assert correct lower-right groups
        self.assertEqual(bo._kill_group(11, 13), 22)
        self.assertEqual(bo._kill_group(14, 13), 17)
        self.assertEqual(bo._array, [
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, W, _, W, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, W, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, W, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
        ])

    def test_get_liberties(self):
        bo = self.get_test_board_1()[0]

        # Assert only black of white group is fetched
        # self.assertRaises(BoardError, bo.get_group, 3, 1)
        # self.assertRaises(BoardError, bo.get_group, 10, 10)

        # Assert empty location returns self as liberty
        self.assertEqual(bo.get_liberties(3, 1), set([(3, 1)]))

        # Assert correct upper-left groups
        self.assertEqual(bo.get_liberties(1, 1), set([
            (1, 2), (2, 2), (3, 1),
        ]))
        self.assertEqual(bo.get_liberties(2, 1), set([
            (1, 2), (2, 2), (3, 1),
        ]))
        self.assertEqual(bo.get_liberties(2, 3), set([
            (1, 3), (1, 4), (2, 2), (2, 5), (3, 3), (3, 4),
        ]))
        self.assertEqual(bo.get_liberties(5, 2), set([
            (4, 2), (5, 1), (6, 2),
        ]))
        self.assertEqual(bo.get_liberties(5, 3), set())
        self.assertEqual(bo.get_liberties(8, 3), set([
            (7, 3), (7, 4), (8, 2), (8, 5), (9, 3), (9, 5), (10, 4),
        ]))
        self.assertEqual(bo.get_liberties(2, 7), set([
            (1, 7), (1, 8), (2, 9),
        ]))
        self.assertEqual(bo.get_liberties(2, 6), set([
            (1, 6),
            (2, 5), (2, 9),
            (3, 5), (3, 10),
            (4, 5), (4, 10),
            (5, 6), (5, 7), (5, 9),
            (6, 6), (6, 9),
            (7, 7), (7, 8),
        ]))

        # # Assert correct lower-right groups
        self.assertEqual(bo.get_liberties(11, 13), set([
            (10, 13), (10, 14), (10, 15), (10, 16), (10, 17), (10, 18), (10, 19),
            (11, 12),
            (12, 12), (12, 14), (12, 18), (12, 19),
            (13, 12),
            (15, 16),
        ]))
        self.assertEqual(bo.get_liberties(14, 13), set([
            (14, 12),
            (15, 12), (15, 14), (15, 15), (15, 16),
            (16, 12),
            (17, 13), (17, 14), (17, 15), (17, 17),
            (18, 16), (18, 18), (18, 19)
        ]))

    def test_count_liberties(self):
        bo = self.get_test_board_1()[0]

        # Assert empty location returns self as liberty (count 1)
        self.assertEqual(bo.count_liberties(3, 1), 1)

        # Assert correct upper-left groups
        self.assertEqual(bo.count_liberties(1, 1), 3)
        self.assertEqual(bo.count_liberties(2, 1), 3)
        self.assertEqual(bo.count_liberties(2, 3), 6)
        self.assertEqual(bo.count_liberties(5, 2), 3)
        self.assertEqual(bo.count_liberties(5, 3), 0)
        self.assertEqual(bo.count_liberties(8, 3), 7)
        self.assertEqual(bo.count_liberties(2, 7), 3)
        self.assertEqual(bo.count_liberties(2, 6), 14)

        # # Assert correct lower-right groups
        self.assertEqual(bo.count_liberties(11, 13), 14)
        self.assertEqual(bo.count_liberties(14, 13), 13)

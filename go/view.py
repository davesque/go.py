from .array import Array
from .board import Board


class View(Array):
    """
    Stores string array which is used to paint the board.  Also stores cursor
    position.
    """
    HOSHI = '+'

    HOSHIS = [
        (4, 4), (10, 4), (16, 4),
        (4, 10), (10, 10), (16, 10),
        (4, 16), (10, 16), (16, 16),
    ]

    CURSOR = 'X'

    def __init__(self, board):
        self._board = board
        self._cursor = (1, 1)

        super(View, self).__init__(
            board._width,
            board._height,
        )

    def _reset(self):
        # Draw pieces from board state
        self._array = [
            [str(pos) for pos in row]
            for row in self._board._array
        ]

        # Draw hoshi points
        for i in self.HOSHIS:
            if self[i] == str(Board.EMPTY):
                self[i] = self.HOSHI

    def redraw(self):
        self._reset()

    def _in_width(self, v):
        return max(1, min(self._width, v))

    def _in_height(self, v):
        return max(1, min(self._height, v))

    def cursor_up(self):
        self._cursor = (
            self._in_width(self._cursor[0]),
            self._in_height(self._cursor[1] - 1),
        )

    def cursor_down(self):
        self._cursor = (
            self._in_width(self._cursor[0]),
            self._in_height(self._cursor[1] + 1),
        )

    def cursor_left(self):
        self._cursor = (
            self._in_width(self._cursor[0] - 1),
            self._in_height(self._cursor[1]),
        )

    def cursor_right(self):
        self._cursor = (
            self._in_width(self._cursor[0] + 1),
            self._in_height(self._cursor[1]),
        )

    @property
    def cursor(self):
        return self._cursor

    def __str__(self):
        arr = self.copy

        if self._cursor:
            arr[self._cursor] = self.CURSOR

        return '\n'.join([' '.join(row) for row in arr._array])

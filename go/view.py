import math

from .array import Array
from .board import Board


class View(Array):
    """
    Stores string array which is used to paint the board.  Also stores cursor
    position.
    """
    HOSHI = '+'

    CURSOR = 'X'

    def __init__(self, board):
        self._board = board
        self._cursor = (1, 1)

        self._hoshis = self._get_hoshis(board._width)

        super(View, self).__init__(
            board._width,
            board._height,
        )

    def _reset(self):
        # Draw pieces from board state
        self._array = [
            [str(loc) for loc in row]
            for row in self._board._array
        ]

        # Draw hoshi points
        for i in self._hoshis:
            if self[i] == str(Board.EMPTY):
                self[i] = self.HOSHI

    def redraw(self):
        self._reset()

    def _get_hoshis(cls, width):
        """
        Calculates and returns hoshi points.
        """
        # The x-coordinate of a left hoshi point.  Roughly equivalent to the
        # floor of the square root of the board width over 0.88.
        left = top = int(math.floor(math.pow(width, 0.5) / 0.88))
        right = bottom = width - left + 1
        middle = width // 2 + 1

        hoshis = tuple()

        # Create corner hoshis
        if width > 3:
            hoshis += (
                (left, top), (right, top),
                (left, bottom), (right, bottom),
            )

        # Create center hoshi
        if width > 7 and width % 2:
            hoshis += ((middle, middle),)

        # Create middle hoshis
        if width > 13 and width % 2:
            hoshis += (
                (left, middle), (middle, top),
                (right, middle), (middle, bottom),
            )

        return hoshis

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

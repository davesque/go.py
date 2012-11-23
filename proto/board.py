from copy import deepcopy
from position import Position
from canvas import Canvas


class BoardView(Canvas):
    # HOSHI = '\033[1m+\033[0m'
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

        super(BoardView, self).__init__(
            board._width * 2 - 1,
            board._height,
        )

        self._width = board._width
        self._height = board._height

    def _reset(self):
        board_canvas = self._board._canvas

        self._canvas = [
            list(' '.join([str(pos) for pos in row]))
            for row in board_canvas
        ]

        for x, y in self.HOSHIS:
            if self.get(x, y) == str(Board.EMPTY):
                self.set(x, y, self.HOSHI)

    def redraw(self):
        self._reset()

    def _array_coords(cls, x, y):
        return x * 2 - 2, y - 1

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
        canvas = deepcopy(self._canvas)

        if self._cursor:
            x, y = self._array_coords(
                self._cursor[0],
                self._cursor[1],
            )
            canvas[y][x] = self.CURSOR

        return '\n'.join([''.join(row) for row in canvas])


class Board(Canvas):
    BLACK = Position('black')
    WHITE = Position('white')
    EMPTY = Position('empty')

    MOVE_POSITIONS = (
        BLACK,
        WHITE,
    )

    class BoardError(Canvas.CanvasError):
        pass

    def move(self, x, y, pos):
        if pos not in self.MOVE_POSITIONS:
            raise self.BoardError('Position \'{0}\' is not one of the following: {1}'.format(
                repr(pos),
                self.MOVE_POSITIONS
            ))

        if self.get(x, y) is not self.EMPTY:
            raise self.BoardError('Cannot move on top of another piece')

    def get_none(self, x, y):
        """
        Same thing as Canvas.get, but returns None if coordinates are not
        within canvas dimensions.
        """
        try:
            return self.get(x, y)
        except Canvas.CanvasError:
            return None

    def get_surrounding(self, x, y):
        """
        Gets information about the surrounding positions for a specified
        coordinate.  Returns a tuple of the positions clockwise starting from
        the top.
        """
        coords = (
            (x, y - 1),
            (x + 1, y),
            (x, y + 1),
            (x - 1, y),
        )
        return [
            (self.get_none(a, b), (a, b))
            for a, b in coords
            if self.get_none(a, b)
        ]

    def _get_liberties(self, x, y, traversed):
        """
        Recursively traverses adjascent positions of the same color to find all
        surrounding liberties for the position at the given coordinates.
        """
        pos = self.get(x, y)

        if pos is self.EMPTY:
            # Return coords of empty position (this counts as a liberty)
            return set([(x, y)])
        else:
            # Get surrounding positions which are empty or have the same color
            # and whose coordinates have not already been traversed
            positions = [
                (p, (a, b))
                for (p, (a, b)) in self.get_surrounding(x, y)
                if (p is pos or p is self.EMPTY) and (a, b) not in traversed
            ]

            # Mark current coordinates as having been traversed
            traversed.add((x, y))

            # Collect unique coordinates of surrounding liberties
            return set.union(*[
                self._get_liberties(a, b, traversed)
                for (_, (a, b)) in positions
            ])

    def get_liberties(self, x, y):
        """
        Gets the coordinates for liberties surrounding the position at the
        given coordinates.
        """
        return self._get_liberties(x, y, set())

    def count_liberties(self, x, y):
        """
        Gets the number of liberties surrounding the position at the
        given coordinates.
        """
        return len(self.get_liberties(x, y))

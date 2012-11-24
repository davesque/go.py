from position import Position
from canvas import Canvas
from utils import intersperse


class BoardView(Canvas):
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
            intersperse(' ', [str(pos) for pos in row])
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
        canvas = self._copy

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

    TURNS = (
        BLACK,
        WHITE,
    )

    class BoardError(Canvas.CanvasError):
        pass

    def __init__(self, *args, **kwargs):
        super(Board, self).__init__(*args, **kwargs)

        self._turn = self.BLACK

        self._black_score = 0
        self._white_score = 0

        self._history = []

    @property
    def turn(self):
        return self._turn

    def move(self, x, y):
        # 1. Check if position is valid
        if self._turn not in self.TURNS:
            raise self.BoardError('Position \'{0}\' must be one of the following: {1}'.format(
                repr(self._turn),
                self.TURNS,
            ))

        # 2. Check if coordinates are occupied
        if self.get(x, y) is not self.EMPTY:
            raise self.BoardError('Cannot move on top of another piece')

        # 3. Check if move is redundant.  A redundant move is one that would
        # return the board to the state at the time of a player's last move.
        check_board = self._copy
        a, b = self._array_coords(x, y)
        check_board[b][a] = self._turn

        try:
            if check_board == self._history[-1][1]:
                raise self.BoardError('Cannot make a move that is redundant')
        except IndexError:
            # No previous board state exists...let this one slide
            pass

        # 4. Check if move is suicidal.  A suicidal move is a move into a
        # position which has no liberties.
        #   - A move may have no liberties and still not be suicidal.  This
        #   would happen if the move reduced the liberties of an enemy group to
        #   zero.

        # 5. Make move
        # Add current board state to history and set move
        self._history.append((self._turn, self._copy))
        self.set(x, y, self._turn)

        # 6. Check if any pieces have been taken:
        #   * get surrounding positions, for each position:
        #     - count liberties for position
        #     - if liberties == zero, remove group for position and add group
        #     count to opponent's score

        # Iterate turn
        self._turn = self.TURNS[self._turn is self.BLACK]

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
        return filter(lambda i: bool(i[0]), [
            (self.get_none(a, b), (a, b))
            for a, b in coords
        ])

    def _get_group(self, x, y, found):
        """
        Recursively traverses adjascent positions of the same color to find all
        positions which are members of the same group.
        """
        pos = self.get(x, y)

        # Get surrounding positions which have the same color and whose
        # coordinates have not already been found
        positions = [
            (p, (a, b))
            for (p, (a, b)) in self.get_surrounding(x, y)
            if p is pos and (a, b) not in found
        ]

        # Add current coordinates to found coordinates
        found.add((x, y))

        # Find coordinates of similar neighbors
        return found.union(*[
            self._get_group(a, b, found)
            for (_, (a, b)) in positions
        ])

    def get_group(self, x, y):
        """
        Gets the coordinates for all positions which are members of the same
        group as the position at the given coordinates.
        """
        pos = self.get(x, y)

        if pos not in (self.WHITE, self.BLACK):
            raise self.BoardError('Can only get group of white or black position')

        return self._get_group(x, y, set())

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

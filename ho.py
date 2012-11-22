class Position(object):
    COLORS = {
        'black': '@',
        'white': 'O',
        'empty': '+',
    }

    class PositionError(Exception):
        pass

    def __init__(self, color):
        if color not in self.COLORS:
            raise self.PositionError('Color must be one of the following: {0}'.format(self.COLORS.keys()))
        self._color = color

    def __eq__(self, other):
        return self._color == other._color

    def __str__(self):
        return self.COLORS[self._color]

    def __repr__(self):
        return '<Position: {0}>'.format(self._color)


class Canvas(object):
    EMPTY = None

    class CanvasError(Exception):
        pass

    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._reset()

    def _reset(self, value=None):
        value = value or self.EMPTY

        self._canvas = [
            [value for i in range(self._width)]
            for j in range(self._height)
        ]

    def _check_coords(self, x, y):
        if (
            x < 1 or
            x > self._width or
            y < 1 or
            y > self._height
        ):
            raise self.CanvasError('Coordinates ({x}, {y}) are not within canvas dimensions {w}x{h}'.format(
                x=x, y=y, w=self._width, h=self._height
            ))

    def set(self, x, y, value):
        self._check_coords(x, y)
        self._canvas[y - 1][x - 1] = value

    def get(self, x, y):
        self._check_coords(x, y)
        return self._canvas[y - 1][x - 1]

    def __eq__(self, other):
        return self._canvas == other._canvas


class BoardCanvas(Canvas):
    HOSHI = '*'
    HOSHIS = [
        (4, 4),
        (10, 4),
        (16, 4),
        (4, 10),
        (10, 10),
        (16, 10),
        (4, 16),
        (10, 16),
        (16, 16),
    ]

    def __init__(self, board):
        self._board = board

        super(BoardCanvas, self).__init__(
            board._width * 2 - 1,
            board._height,
        )

    def _reset(self):
        board_canvas = self._board._canvas

        self._canvas = [
            list('-'.join([str(pos) for pos in row]))
            for row in board_canvas
        ]

        for x, y in self.HOSHIS:
            if self.get(x, y) == '+':
                self.set(x, y, self.HOSHI)

    def set(self, x, y, value):
        x = 2 * x - 1
        super(BoardCanvas, self).set(x, y, value)

    def get(self, x, y):
        x = 2 * x - 1
        return super(BoardCanvas, self).get(x, y)

    def __str__(self):
        return '\n'.join([''.join(row) for row in self._canvas])


class Board(Canvas):
    BLACK = Position('black')
    WHITE = Position('white')
    EMPTY = Position('empty')

    class BoardError(Canvas.CanvasError):
        pass


b = Board(19, 19)
c = BoardCanvas(b)

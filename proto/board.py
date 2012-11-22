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

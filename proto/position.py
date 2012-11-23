class Position(object):
    COLORS = {
        'black': '@',
        'white': 'O',
        'empty': '.',
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

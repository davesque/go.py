from copy import copy


class ArrayError(Exception):
    pass


class Array(object):
    def __init__(self, width, height, empty=None):
        self._width = width
        self._height = height
        self._empty = empty

        self._reset()

    def _reset(self, value=None):
        value = value or self._empty

        self._array = [
            [value for i in range(self._width)]
            for j in range(self._height)
        ]

    def _check_index(self, x, y):
        if (
            x < 1 or
            x > self._width or
            y < 1 or
            y > self._height
        ):
            raise ArrayError('Index is not within array dimensions {w}x{h}'.format(
                x=x, y=y, w=self._width, h=self._height
            ))

    def _zero_index(cls, x, y):
        return x - 1, y - 1

    def __getitem__(self, i):
        self._check_index(*i)
        x, y = self._zero_index(*i)
        return self._array[y][x]

    def __setitem__(self, i, value):
        self._check_index(*i)
        x, y = self._zero_index(*i)
        self._array[y][x] = value

    def __eq__(self, other):
        return self._array == other._array

    @property
    def copy(self):
        new = copy(self)
        new._array = [copy(row) for row in self._array]
        return new

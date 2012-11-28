from utils import bold


class PositionError(Exception):
    pass


class Position(object):
    TYPES = {
        'black': bold('@'),
        'white': bold('O'),
        'empty': '.',
    }

    def __init__(self, type):
        if type not in self.TYPES:
            raise PositionError('Type must be one of the following: {0}'.format(
                self.TYPES.keys(),
            ))
        self._type = type

    def __eq__(self, other):
        return self._type == other._type

    def __hash__(self):
        return hash(self._type)

    def __str__(self):
        return self.TYPES[self._type]

    def __repr__(self):
        return self._type.title()

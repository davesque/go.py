from collections import namedtuple
from copy import copy

from .array import Array, ArrayError
from .position import Position


class BoardError(Exception):
    pass


class Board(Array):
    """
    Stores board positions.  Provides methods to carry out game logic.
    """
    BLACK = Position('black')
    WHITE = Position('white')
    EMPTY = Position('empty')

    TURNS = (
        BLACK,
        WHITE,
    )

    State = namedtuple('State', ['board', 'turn', 'score'])

    def __init__(self, *args, **kwargs):
        kwargs['empty'] = self.EMPTY

        super(Board, self).__init__(*args, **kwargs)

        # Turn counter
        self._turn = self.BLACK

        # Player scores
        self._score = {
            self.BLACK: 0,
            self.WHITE: 0,
        }

        # Game history
        self._history = []
        self._redo = []

    @property
    def turn(self):
        """
        Gets the current turn.
        """
        return repr(self._turn)

    @property
    def score(self):
        """
        Gets the current score.
        """
        return {
            'black': self._score[self.BLACK],
            'white': self._score[self.WHITE],
        }

    def move(self, x, y):
        """
        Makes a move at the given position for the current turn's color.
        """
        # Check if coordinates are occupied
        if self[(x, y)] is not self.EMPTY:
            raise BoardError('Cannot move on top of another piece!')

        # Store history and make move
        self._push_history()
        self[(x, y)] = self._turn

        # Check if any pieces have been taken
        taken = self._take_pieces(x, y)

        # Check if move is suicidal.  A suicidal move is a move that takes no
        # pieces and is played on a coordinate which has no liberties.
        if taken == 0:
            self._check_for_suicide(x, y)

        # Check if move is redundant.  A redundant move is one that would
        # return the board to the state at the time of a player's last move.
        self._check_for_redundancy()

        self._flip_turn()
        self._redo = []

    def _check_for_suicide(self, x, y):
        """
        Checks if move is suicidal.
        """
        if self.count_liberties(x, y) == 0:
            self._pop_history()
            raise BoardError('Cannot play on position with no liberties!')

    def _check_for_redundancy(self):
        """
        Checks if board state is redundant.
        """
        try:
            if self._array == self._history[-2][0]:
                self._pop_history()
                raise BoardError('Cannot make a move that is redundant!')
        except IndexError:
            # Insufficient history...let this one slide
            pass

    def _take_pieces(self, x, y):
        """
        Checks if any pieces were taken by the last move at the specified
        coordinates.  If so, removes them from play and tally resulting points.
        """
        scores = []
        for (p, (x1, y1)) in self._get_surrounding(x, y):
            if p is not self.EMPTY:
                liberties = self.count_liberties(x1, y1)
                if liberties == 0:
                    score = self._kill_group(x1, y1)
                    scores.append(score)
                    self._tally(score)
        return sum(scores)

    def _flip_turn(self):
        """
        Iterates the turn counter.
        """
        self._turn = self.TURNS[self._turn is self.BLACK]
        return self._turn

    @property
    def _state(self):
        """
        Returns the game state as a named tuple.
        """
        return self.State(self.copy._array, self._turn, copy(self._score))

    def _load_state(self, state):
        """
        Loads the specified game state.
        """
        self._array, self._turn, self._score = state

    def _push_history(self):
        """
        Pushes game state onto history.
        """
        self._history.append(self._state)

    def _pop_history(self):
        """
        Pops and loads game state from history.
        """
        current_state = self._state
        try:
            self._load_state(self._history.pop())
            return current_state
        except IndexError:
            return None

    def undo(self):
        """
        Undoes one move.
        """
        state = self._pop_history()
        if state:
            self._redo.append(state)
            return state
        else:
            raise BoardError('No moves to undo!')

    def redo(self):
        """
        Re-applies one move that was undone.
        """
        try:
            self._push_history()
            self._load_state(self._redo.pop())
        except IndexError:
            self._pop_history()
            raise BoardError('No undone moves to redo!')

    def _tally(self, score):
        """
        Adds points to the current turn's score.
        """
        self._score[self._turn] += score

    def _get_none(self, x, y):
        """
        Same thing as Array.__getitem__, but returns None if coordinates are
        not within array dimensions.
        """
        try:
            return self[(x, y)]
        except ArrayError:
            return None

    def _get_surrounding(self, x, y):
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
            (self._get_none(a, b), (a, b))
            for a, b in coords
        ])

    def _get_group(self, x, y, found):
        """
        Recursively traverses adjascent positions of the same color to find all
        positions which are members of the same group.
        """
        pos = self[(x, y)]

        # Get surrounding positions which have the same color and whose
        # coordinates have not already been found
        positions = [
            (p, (a, b))
            for (p, (a, b)) in self._get_surrounding(x, y)
            if p is pos and (a, b) not in found
        ]

        # Add current coordinates to found coordinates
        found.add((x, y))

        # Find coordinates of similar neighbors
        if positions:
            return found.union(*[
                self._get_group(a, b, found)
                for (_, (a, b)) in positions
            ])
        else:
            return found

    def get_group(self, x, y):
        """
        Gets the coordinates for all positions which are members of the same
        group as the position at the given coordinates.
        """
        if self[(x, y)] not in self.TURNS:
            raise BoardError('Can only get group for black or white position')

        return self._get_group(x, y, set())

    def _kill_group(self, x, y):
        """
        Kills a group of black or white pieces and returns its size for
        scoring.
        """
        if self[(x, y)] not in self.TURNS:
            raise BoardError('Can only kill black or white group')

        group = self.get_group(x, y)
        score = len(group)

        for (x1, y1) in group:
            self[(x1, y1)] = self.EMPTY

        return score

    def _get_liberties(self, x, y, traversed):
        """
        Recursively traverses adjascent positions of the same color to find all
        surrounding liberties for the position at the given coordinates.
        """
        pos = self[(x, y)]

        if pos is self.EMPTY:
            # Return coords of empty position (this counts as a liberty)
            return set([(x, y)])
        else:
            # Get surrounding positions which are empty or have the same color
            # and whose coordinates have not already been traversed
            positions = [
                (p, (a, b))
                for (p, (a, b)) in self._get_surrounding(x, y)
                if (p is pos or p is self.EMPTY) and (a, b) not in traversed
            ]

            # Mark current coordinates as having been traversed
            traversed.add((x, y))

            # Collect unique coordinates of surrounding liberties
            if positions:
                return set.union(*[
                    self._get_liberties(a, b, traversed)
                    for (_, (a, b)) in positions
                ])
            else:
                return set()

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

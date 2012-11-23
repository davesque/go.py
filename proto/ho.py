#!/usr/bin/env python

import sys

from board import Board, BoardView
from utils import clear, getch


KEYS = {
    'w': 'cursor_up',
    'r': 'cursor_down',
    'a': 'cursor_left',
    's': 'cursor_right',
    'x': None,
    '\x1b': None,
}


TURNS = (
    Board.BLACK,
    Board.WHITE,
)

turn = Board.BLACK


def main():
    board = Board(19, 19)
    view = BoardView(board)

    def move():
        global turn

        x, y = view.cursor
        board.set(x, y, turn)

        view.redraw()

        turn = TURNS[turn is Board.BLACK]

    def exit():
        sys.exit(0)

    KEYS['x'] = move
    KEYS['\x1b'] = exit

    while True:
        clear()

        # Print board
        print view
        print 'Make your move... '

        # Get char
        c = getch()

        # Move cursor
        try:
            getattr(view, KEYS[c])()
        except (TypeError, AttributeError):
            KEYS[c]()
        except KeyError:
            pass


if __name__ == '__main__':
    main()

#!/usr/bin/env python

import sys

from board import Board, BoardView
from utils import clear, getch


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

    KEYS = {
        'w': view.cursor_up,
        'r': view.cursor_down,
        'a': view.cursor_left,
        's': view.cursor_right,
        'x': move,
        '\x1b': exit,
    }

    while True:
        # Print board
        clear()
        print view
        sys.stdout.write('{0}\'s move... '.format(repr(turn)))

        # Get action
        c = getch()

        try:
            # Execute selected action
            KEYS[c]()
        except KeyError:
            # Action not found, do nothing
            pass


if __name__ == '__main__':
    main()

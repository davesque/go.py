#!/usr/bin/env python

import sys

from board import Board, BoardView
from utils import clear, getch


group = None


def main():
    global group

    board = Board(19, 19)
    view = BoardView(board)

    def move():
        board.move(*view.cursor)
        view.redraw()

    def exit():
        sys.exit(0)

    def get_group():
        global group
        x, y = view.cursor
        group = board.get_group(x, y)

    KEYS = {
        'w': view.cursor_up,
        'r': view.cursor_down,
        'a': view.cursor_left,
        's': view.cursor_right,
        'x': move,
        '\x1b': exit,
        'g': get_group,
    }

    while True:
        # Print board
        clear()
        print view
        sys.stdout.write('{0}\n'.format(group))
        sys.stdout.write('{0}\'s move... '.format(repr(board.turn)))

        group = None

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

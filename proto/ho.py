#!/usr/bin/env python

from board import Board, BoardView
from utils import clear, getch


KEYS = {
    'w': 'cursor_up',
    'r': 'cursor_down',
    'a': 'cursor_left',
    's': 'cursor_right',
    '\x1b': 'exit',
}


def main():
    board = Board(19, 19)
    view = BoardView(board)

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
        except KeyError:
            pass
        except AttributeError:
            if KEYS[c] == 'exit':
                break


if __name__ == '__main__':
    main()

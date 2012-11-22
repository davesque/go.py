#!/usr/bin/env python

import platform
import subprocess
import sys
from copy import deepcopy

from board import Board, BoardCanvas


def clear():
    subprocess.check_call('cls' if platform.system() == 'Windows' else 'clear', shell=True)


class _Getch:
    """
    Gets a single character from standard input.  Does not echo to the
    screen.
    """
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __call__(self):
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt  # NOQA

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()


WIDTH = 19
HEIGHT = 19


def trunc_width(v):
    return max(1, min(WIDTH, v))


def trunc_height(v):
    return max(1, min(HEIGHT, v))


def move_up(x, y):
    return trunc_width(x), trunc_height(y - 1)


def move_down(x, y):
    return trunc_width(x), trunc_height(y + 1)


def move_left(x, y):
    return trunc_width(x - 1), trunc_height(y)


def move_right(x, y):
    return trunc_width(x + 1), trunc_height(y)


KEYS = {
    'w': move_up,
    'r': move_down,
    'a': move_left,
    's': move_right,
}


def main():
    board = Board(WIDTH, HEIGHT)
    canvas = BoardCanvas(board)

    cur_x, cur_y = (1, 1)

    while True:
        clear()

        # Print board
        select_board = deepcopy(canvas)
        select_board.set(cur_x, cur_y, 'X')
        print select_board
        print 'Make your move... '

        # Get char
        c = getch()

        # Escape terminates
        if c == '\x1b':
            break

        # Move cursor
        try:
            cur_x, cur_y = KEYS[c](cur_x, cur_y)
        except KeyError:
            pass

if __name__ == '__main__':
    main()

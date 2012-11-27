import platform
import subprocess


def bold(v):
    return '\033[1m{0}\033[0m'.format(v)


def clear():
    subprocess.check_call('cls' if platform.system() == 'Windows' else 'clear', shell=True)


def intersperse(x, xs):
    return sum([[i, x] for i in xs], [])[:-1]


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
        import sys
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

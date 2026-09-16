import curses

ORANGE = None
RED = None
GREEN = None
YELLOW = None
WHITE = None
CYAN_MAGENTA = None
RED_GREEN = None
PURPLE = None


def init_colors():
    """Initialize curses colors and expose them as module-level color constants."""
    global ORANGE, RED, GREEN, YELLOW, WHITE, CYAN_MAGENTA, RED_GREEN, PURPLE

    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_MAGENTA)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_GREEN)
    CYAN_MAGENTA_1 = curses.color_pair(1)
    RED_GREEN_1 = curses.color_pair(2)

    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)
    curses.init_pair(5, curses.COLOR_RED, -1)
    curses.init_pair(6, curses.COLOR_WHITE, -1)
    curses.init_pair(8, curses.COLOR_MAGENTA, -1)
    GREEN_1 = curses.color_pair(3)
    YELLOW_1 = curses.color_pair(4)
    RED_1 = curses.color_pair(5)
    WHITE_1 = curses.color_pair(6)
    PURPLE_1 = curses.color_pair(8)

    ORANGE_COLOR_CODE = 208
    curses.init_color(208, 1000, 647, 0)
    curses.init_pair(7, ORANGE_COLOR_CODE, -1)
    ORANGE_1 = curses.color_pair(7)

    # Assign final values back to the module-level names.
    ORANGE = ORANGE_1
    RED = RED_1
    GREEN = GREEN_1
    YELLOW = YELLOW_1
    WHITE = WHITE_1
    CYAN_MAGENTA = CYAN_MAGENTA_1
    RED_GREEN = RED_GREEN_1
    PURPLE = PURPLE_1

"""
Basic VT-100/ANSI terminal functionality for Python running in a console.

No object-orientation here: this simply provides functionality for easy
construction of appropriate escape sequence.  If you want state or something as
sophisticated as curses, this is not the module you're looking for.
"""

import sys

# Start of all VT-100 command sequences.
ESC = chr(27) + '['

# Also used as parameters to Color.  Note that these codes match the original
# IBM PC CGA colors.
COLOR_BLACK   = 0
COLOR_RED     = 1
COLOR_GREEN   = 2
COLOR_YELLOW  = 3
COLOR_BLUE    = 4
COLOR_MAGENTA = 5
COLOR_CYAN    = 6
COLOR_WHITE   = 7

# Modify foreground color (normal intensity).
BLACK   = ESC + '3' + str(COLOR_BLACK)   + ';22m'
RED     = ESC + '3' + str(COLOR_RED)     + ';22m'
GREEN   = ESC + '3' + str(COLOR_GREEN)   + ';22m'
YELLOW  = ESC + '3' + str(COLOR_YELLOW)  + ';22m'
BLUE    = ESC + '3' + str(COLOR_BLUE)    + ';22m'
MAGENTA = ESC + '3' + str(COLOR_MAGENTA) + ';22m'
CYAN    = ESC + '3' + str(COLOR_CYAN)    + ';22m'
WHITE   = ESC + '3' + str(COLOR_WHITE)   + ';22m'

# Modify foreground color (high intensity).
BOLD_BLACK   = ESC + '3' + str(COLOR_BLACK)   + ';1m'
BOLD_RED     = ESC + '3' + str(COLOR_RED)     + ';1m'
BOLD_GREEN   = ESC + '3' + str(COLOR_GREEN)   + ';1m'
BOLD_YELLOW  = ESC + '3' + str(COLOR_YELLOW)  + ';1m'
BOLD_BLUE    = ESC + '3' + str(COLOR_BLUE)    + ';1m'
BOLD_MAGENTA = ESC + '3' + str(COLOR_MAGENTA) + ';1m'
BOLD_CYAN    = ESC + '3' + str(COLOR_CYAN)    + ';1m'
BOLD_WHITE   = ESC + '3' + str(COLOR_WHITE)   + ';1m'

def Color(fg, bg=COLOR_BLACK):
    """Set the foreground and background colors."""
    return ESC + str(fg+30) + ';' + str(bg+40) + 'm'

# Turn off all attributes, but preserve current color.
NORMAL = ESC + '22;24;25;27m'

# Turn off all attributes, including color.
RESET = ESC + '0;37m'

# Turn on/off bolding.
BOLD   = ESC + '1m'
NOBOLD = ESC + '22m'

# Turn on/off blink.  Often not supported; don't expect this to work.
BLINK   = ESC + '5m'
NOBLINK = ESC + '25m'

# Turn on/off reverse mode.
REVERSE   = ESC + '7m'
NOREVERSE = ESC + '27m'

# Turn on/off underline mode.  Often not supported; don't expect this to work.
UNDERLINE   = ESC + '4m'
NOUNDERLINE = ESC + '24m'

# Clear parts of the screen.
CLEAR      = ESC + '2J'  # whole screen
CLEAR_EOL  = ESC + '0K'  # to end of line
CLEAR_EOS  = ESC + '0J'  # to end of screen
CLEAR_LINE = ESC + '2K'  # entire line

# Cursor control.
HOME  = ESC + '1;1H'  # upper-left corner
UP    = ESC + '1A'    # up one row
DOWN  = ESC + '1B'    # down one row
LEFT  = ESC + '1D'    # left one column
RIGHT = ESC + '1C'    # right one column

def Up(n=1):
    """Move the cursor up |n| rows."""
    return ESC + str(n) + 'A'
    
def Down(n=1):
    """Move the cursor down |n| rows."""
    return ESC + str(n) + 'B'

def Left(n=1):
    """Move the cursor left |n| columns."""
    return ESC + str(n) + 'D'
    
def Right(n=1):
    """Move the cursor right |n| columns."""
    return ESC + str(n) + 'C'
    
def XY(x, y):
    """Move the cursor to the zero-based location (x, y)."""
    return ESC + str(y + 1) + ';' + str(x + 1) + 'H'
    
def Pos(row, col):
    """Move the cursor to the one-based location (col, row)."""
    return ESC + str(row) + ';' + str(col) + 'H'

def Write(*args):
    """Convenience function to write all arguments directly to sys.stdout."""
    for arg in args:
        sys.stdout.write(str(arg))
    
def WriteLn(*args):
    """Like Write, but also ends the line."""
    for arg in args:
        sys.stdout.write(str(arg))
    sys.stdout.write('\n')

import random

from .. import common
from .. import term

VERSION = '0.0.2'

# Status values stored within the maze array.
WALL  = 0
SPACE = 1
CRUMB = 2

# Symbolic constants for the directions; used as indices into OFFSET.
UP    = 0
DOWN  = 1
LEFT  = 2
RIGHT = 3

# (row, col) deltas for each direction, to simplify array access.
DELTA = ( (-1, 0), (1, 0), (0, -1), (0, 1) )

class Maze():
    """Class representing the constructed maze."""
    
    def __init__(self, rows, cols):
        """Initializes the maze as a solid block of walls."""
        self.rows = rows
        self.cols = cols
        self.maze = []
        for row in xrange(self.rows):
            self.maze.append([WALL] * self.cols)

    def CanDig(self, row, col, dir):
        """Is it possible to dig in the given direction?"""
        row += 2 * DELTA[dir][0]
        col += 2 * DELTA[dir][1]
        return ((row > 0) and (row < self.rows) and
                (col > 0) and (col < self.cols) and
                self.maze[row][col] == WALL)

    def Dig(self, row, col, dir):
        """Actually digs in the given direction.  Assumes that we can."""
        self.maze[row                  ][col                  ] = SPACE
        self.maze[row +   DELTA[dir][0]][col +   DELTA[dir][1]] = CRUMB
        self.maze[row + 2*DELTA[dir][0]][col + 2*DELTA[dir][1]] = SPACE

    def Generate(self):
        """Generate a maze that completely fills our available space."""
        row  = 1
        col  = 1
        done = False

        while not done:
            ok = []
            for dir in xrange(4):
                if self.CanDig(row, col, dir):
                    ok.append(dir)

            if ok:
                dir = random.choice(ok)
                self.Dig(row, col, dir)
                row += 2 * DELTA[dir][0]
                col += 2 * DELTA[dir][1]
            elif (row == 1) and (col == 1):
                done = True
            else:
                for dir in xrange(4):
                    nrow = row + DELTA[dir][0]
                    ncol = col + DELTA[dir][1]
                    if self.maze[nrow][ncol] == CRUMB:
                        self.maze[nrow][ncol] = SPACE
                        row += 2 * DELTA[dir][0]
                        col += 2 * DELTA[dir][1]
                        break

        self.maze[0][1] = SPACE
        self.maze[self.rows - 1][self.cols - 2] = SPACE

    def Print(self):
        term.Write(term.CLEAR, term.BOLD_WHITE)
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                if self.maze[row][col] == WALL:
                    term.Write(term.REVERSE)
                else:
                    term.Write(term.NOREVERSE)
                term.Write(' ')
            term.WriteLn(term.RESET)


def GetSize(which, min, max):
    prompt = 'Enter %s (%d-%d):' % (which, min, max)
    return common.InputInt(prompt, min, max)

def Instructions():
    print "The computer will generate a maze of the complexity you specify."
    print "There will be only one path through the maze, and an infinite"
    print "variety of mazes can be generated."
    print

#------------------------------------------------------------------------

def Run():
    common.Hello('Amazing Maze Generator', VERSION)
    Instructions()

    cols = GetSize('width',  1, 39) * 2 + 1
    rows = GetSize('height', 1, 39) * 2 + 1

    maze = Maze(rows, cols)
    maze.Generate()
    maze.Print()

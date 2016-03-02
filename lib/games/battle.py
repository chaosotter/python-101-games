import random

from .. import common
from .. import term

VERSION = '0.0.1'

# Size of the board and the individual ships.
SIZE = 6
SHIPS = (2, 2, 3, 3, 4, 4)

# (x, y) deltas for the eight directions.
DELTA = ((1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1))


class Board:
    """Encapsulates the current state of the game board."""
    
    def __init__(self, size):
        """Create a new board with all ships still floating."""
        self.size = size
        self.board = []
        for _ in xrange(size):
            self.board.append([0] * size)

        self.left = []
        for ship in xrange(len(SHIPS)):
            self.PlaceShip(ship + 1, SHIPS[ship])
            self.left.append(SHIPS[ship])

    def Bomb(self, row, col):
        """If we bomb (col, row), what ship do we hit?"""
        if self.board[row][col] == 0:
            ship = 0
        else:
            ship = self.board[row][col]
            self.left[ship - 1] -= 1
        self.board[row][col] = 0
        return ship

    def Done(self):
        """Are all ships sunk?"""
        return sum(self.left) == 0

    def PickLocation(self):
        """Select a random location and orientation."""
        return (random.randint(0, self.size - 1),
                random.randint(0, self.size - 1),
                random.randint(0, 7))

    def PlacementOkay(self, ship_size, row, col, dir):
        """Verifies that a hypothetical placement is possible."""
        for i in xrange(ship_size):
            if ((row < 0) or (row >= self.size) or
                (col < 0) or (col >= self.size) or (self.board[row][col] != 0)):
                return False
            row += DELTA[dir][1]
            col += DELTA[dir][0]
        return True

    def PlaceShip(self, ship, ship_size):
        """Find a home for a ship of this size."""
        (row, col, dir) = self.PickLocation()
        while not self.PlacementOkay(ship_size, row, col, dir):
            (row, col, dir) = self.PickLocation()
        for i in xrange(ship_size):
            self.board[row][col] = ship
            row += DELTA[dir][1]
            col += DELTA[dir][0]

    def PrintBoard(self):
        """Print out a thinly-veiled hint."""
        term.WriteLn("\n\nThis coded map of the computer's fleet layout was intercepted,")
        term.WriteLn("but our code experts haven't been able to figure it out!\n")
        for row in self.board:
            term.Write(term.BOLD_WHITE, ' ')
            for col in row:
                term.Write(col, ' ')
            term.WriteLn(term.RESET)

    def PrintLosses(self):
        """Summarize the state of the game."""
        term.Write("So far, I've lost ")
        losses = []

        if self.Sunk(1) or self.Sunk(2):
            if self.Sunk(1) and self.Sunk(2):
                losses.append('two destroyers')
            else:
                losses.append('a destroyer')
        
        if self.Sunk(3) or self.Sunk(4):
            if self.Sunk(3) and self.Sunk(4):
                losses.append('two cruisers')
            else:
                losses.append('a cruiser')

        if self.Sunk(5) or self.Sunk(6):
            if self.Sunk(5) and self.Sunk(6):
                losses.append('two aircraft carriers')
            else:
                losses.append('an aircraft carrier')

        if len(losses) == 3:
            term.WriteLn(losses[0], ', ', losses[1], ', and ', losses[2], '.')
        elif len(losses) == 2:
            term.WriteLn(losses[0], ' and ', losses[1], '.')
        else:
            term.WriteLn(losses[0], '.')

    def Sunk(self, ship):
        """Has this ship been sunk?"""
        return self.left[ship - 1] == 0


def Instructions():
    print "This is an educational variant on the popular board game 'Battleship'."
    print "The computer will place six ships in a six-by-six matrix:"
    print
    print "  Ships 1 and 2: Destroyers (two spaces long)"
    print "  Ships 3 and 4: Cruisers (three spaces long)"
    print "  Ships 5 and 6: Aircraft carriers (four spaces long)"
    print
    print "Your job is to sink the ships by entering the coordinates of the"
    print "location where you want to drop a bomb.  The computer will let you"
    print "know whether you scored a hit or not, and on which ship."
    print
    print "Try to get the best splash-to-hit ratio you can!"
    print

#------------------------------------------------------------------------

def Run():
    common.Hello('Battle', VERSION)
    Instructions()

    board = Board(SIZE)
    if common.InputYN('Show coded map (good for younger players)?'):
        board.PrintBoard()
    term.WriteLn()

    hit = 0
    miss = 0
    while not board.Done():
        row = common.InputInt('Enter row to bomb (1-%d):' % SIZE, 1, SIZE) - 1
        col = common.InputInt('Enter column to bomb (1-%d):' % SIZE, 1, SIZE) - 1

        ship = board.Bomb(row, col)
        if ship == 0:
            term.WriteLn(term.BOLD_RED, 'Splash!  Try again.')
            miss += 1
        else:
            term.WriteLn(term.BOLD_GREEN, 'A direct hit on ship #', ship, '!')
            hit += 1
            if board.Sunk(ship):
                term.WriteLn(term.BOLD_WHITE,
                             'And you sank it!  Hurrah for the good guys!')
                board.PrintLosses()

        term.WriteLn(term.RESET)
        term.Write('Your current splash-to-hit ratio is ', term.BOLD_CYAN)
        if hit == 0:
            term.WriteLn(0, term.RESET)
        else:
            term.WriteLn(float(miss) / hit, term.RESET)

    term.WriteLn(term.BOLD_WHITE)
    term.WriteLn("VICTORY!  You have wiped out the computer's fleet!")
    term.WriteLn(term.RESET)

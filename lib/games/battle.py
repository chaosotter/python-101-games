import lib.ansi, lib.squunkin, random

ansi    = lib.ansi.Ansi()
VERSION = "0.01"

SIZE   = 6
SHIPS  = [ 2, 2, 3, 3, 4, 4 ]

OFFSET = [ [1,0], [1,-1], [0,-1], [-1,-1], [-1,0], [-1,1], [0,1], [1,1] ]


def instructions():
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

class Board:

    def __init__(self, size):

        self.size  = size
        
        self.board = []
        for row in xrange(0, size):
            self.board.append([])
            for col in xrange(0, size):
                self.board[row].append(0)

        self.left  = []
        for ship in xrange(0, len(SHIPS)):
            self.placeShip(ship + 1, SHIPS[ship])
            self.left.append(SHIPS[ship])


    def bomb(self, row, col):
        if self.board[row][col] == 0:
            ship = 0
        else:
            ship = self.board[row][col]
            self.left[ship - 1] -= 1
        self.board[row][col] = 0
        return ship


    def done(self):
        return sum(self.left) == 0


    def pickLocation(self):
        return (random.randint(0, self.size - 1), \
                random.randint(0, self.size - 1), \
                random.randint(0, 7))


    def placementOkay(self, shipSize, row, col, dir):
        for i in xrange(0, shipSize):
            if (row < 0) or (row >= self.size) or \
               (col < 0) or (col >= self.size) or (self.board[row][col] != 0):
                return False
            row += OFFSET[dir][1]
            col += OFFSET[dir][0]
        return True
    

    def placeShip(self, ship, shipSize):
        (row, col, dir) = self.pickLocation()
        while not self.placementOkay(shipSize, row, col, dir):
            (row, col, dir) = self.pickLocation()
        for i in xrange(0, shipSize):
            self.board[row][col] = ship
            row += OFFSET[dir][1]
            col += OFFSET[dir][0]


    def printBoard(self):
        print "\n\nThis coded map of the computer's fleet layout was intercepted,"
        print "but our code experts haven't been able to figure it out!\n"
        for row in self.board:
            print ansi.boldWhite(), "",
            for col in row:
                print col, '',
            print ansi.reset()


    def printLosses(self):
        print "So far, I've lost",
        losses = []

        if self.sunk(1) or self.sunk(2):
            if self.sunk(1) and self.sunk(2):
                losses.append("two destroyers")
            else:
                losses.append("a destroyer")
        
        if self.sunk(3) or self.sunk(4):
            if self.sunk(3) and self.sunk(4):
                losses.append("two cruisers")
            else:
                losses.append("a cruiser")

        if self.sunk(5) or self.sunk(6):
            if self.sunk(5) and self.sunk(6):
                losses.append("two aircraft carriers")
            else:
                losses.append("an aircraft carrier")

        if len(losses) == 3:
            print losses[0] + ", " + losses[1] + ", and " + losses[2] + "."
        elif len(losses) == 2:
            print losses[0] + " and " + losses[1] + "."
        else:
            print losses[0] + "."


    def sunk(self, ship):
        return self.left[ship - 1] == 0


#------------------------------------------------------------------------

lib.squunkin.hello("Battle", VERSION)
instructions()

board = Board(SIZE)

if lib.squunkin.inputYN("Show coded map (good for younger players)?"):
    board.printBoard()
print

hit  = 0
miss = 0

while not board.done():

    prompt = "Enter row to bomb (1-" + str(SIZE) + "):"
    row = lib.squunkin.inputNumber(prompt, 1, SIZE) - 1

    prompt = "Enter column to bomb (1-" + str(SIZE) + "):"
    col = lib.squunkin.inputNumber(prompt, 1, SIZE) - 1

    ship = board.bomb(row, col)
    if ship == 0:
        print ansi.boldRed() + "Splash!  Try again."
        miss += 1
    else:
        print ansi.boldGreen() + "A direct hit on ship #" + str(ship) + "!"
        hit  += 1
        if board.sunk(ship):
            print ansi.boldWhite() + "And you sank it!  Hurrah for the good guys!"
            board.printLosses()

    print ansi.reset() + "\nYour current splash-to-hit ratio is" + ansi.boldCyan(),
    if hit == 0:
        print 0, ansi.reset()
    else:
        print (miss + 0.0) / hit, ansi.reset()

print ansi.boldWhite() + "\nVICTORY!  You have wiped out the computer's fleet!"
print ansi.reset()

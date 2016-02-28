import lib.ansi, lib.squunkin

ansi    = lib.ansi.Ansi()
VERSION = "0.01"

HUMAN      = 0
COMPUTER   = 1
HOME       = [6, 13]

NOWHERE    = -1
VALUE_LOSE = -100
VALUE_WIN  = +100


def computerMove(board):
    if board.again:
        print ansi.boldWhite() + "\nSecond move!"
    else:
        print "My move..."
    move = minimax(Board(board), 7)
    print ansi.boldGreen() + "\nI select the pit opposite #" + str(13 - move)
    return move
    
    
def humanMove(board):
    if board.again:
        print ansi.boldWhite() + "\nSecond move!\n"
    move = 0
    while not board.isLegal(move - 1):
        move = lib.squunkin.inputNumber("Your move (1-6)?", 1, 6)
    return move - 1

        
def instructions():
    print "Awari is a traditional African game played with 36 stones and"
    print "14 pits.  Each player has six pits on their side of the board,"
    print "plus a special 'home' pit that represents their score."
    print
    print "On your move, you take all of the stones from one of your pits "
    print "(other than the home pit) and distribute them among the other "
    print "pits, working counter-clockwise around the board."
    print
    print "If your last stone lands in your home pits, you get a second move."
    print "If it lands in an empty pit, you capture both that stone and all"
    print "the stones in the opposite pit."
    print
    print "Whoever has the most stones in their home when there are no "
    print "moves remaining wins.  (Beware, the computer is a tough opponent!)"
    lib.squunkin.delay()


def maxMove(board, depth):

    # if we're done searching or the game is over, use the current state
    if (depth == 0) or board.gameOver():
        return Move(board.last, board.eval())

    # if there's no move, switch sides and try again
    if not board.hasMove():
        board.turn = other(board.turn)
        board.again = False
        return minMove(board, depth)

    # start with a sentinel move
    best = Move(NOWHERE, VALUE_LOSE - 1)

    # for each potential move
    for offset in range(1, 7):

        # make sure it's a legal move
        location = HOME[board.turn] - offset
        if board.pits[location] == 0:
            continue

        # calculate its effect on the game state
        next = Board(board, location)

        # and evaluate that state
        if next.again:
            move = maxMove(next, depth - 1)
        else:
            move = minMove(next, depth - 1)
        if move.value > best.value:
            best = Move(location, move.value)

    # all done
    return best


def minMove(board, depth):

    # if we're done searching or the game is over, use the current state
    if (depth == 0) or board.gameOver():
        return Move(board.last, board.eval())

    # if there's no move, switch sides and try again
    if not board.hasMove():
        board.turn = other(board.turn)
        board.again = False
        return maxMove(board, depth)

    # start with a sentinel move
    worst = Move(NOWHERE, VALUE_WIN + 1)

    # for each potential move
    for offset in range(1, 7):

        # make sure it's a legal move
        location = HOME[board.turn] - offset
        if board.pits[location] == 0:
            continue

        # calculate its effect on the game state
        next = Board(board, location)

        # and evaluate that state
        if next.again:
            move = minMove(next, depth - 1)
        else:
            move = maxMove(next, depth - 1)
        if move.value < worst.value:
            worst = Move(location, move.value)

    # all done
    return worst


def minimax(board, depth):
    return maxMove(board, depth).location


def other(turn):
    return (turn + 1) % 2


#------------------------------------------------------------------------

class Move:
    def __init__(self, location, value):
        self.location = location
        self.value    = value


#------------------------------------------------------------------------

class Board:

    def __init__(self, *previous):

        # new game
        if len(previous) == 0:
            self.pits  = [ 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0 ]
            self.turn  = HUMAN
            self.last  = -1
            self.again = False
            
        # copy of board
        elif len(previous) == 1:
            self.pits  = list(previous[0].pits)
            self.turn  = previous[0].turn
            self.last  = previous[0].last
            self.again = previous[0].again

        # new move
        else:
            self.pits  = list(previous[0].pits)
            self.turn  = previous[0].turn
            self.again = previous[0].again
            self.apply(previous[1])
            self.last  = previous[1]


    def apply(self, move):

        # distribute the stones
        current = move
        while self.pits[move] > 0:
            current = (current + 1) % 14
            self.pits[move]    -= 1
            self.pits[current] += 1

        # handle capture
        if (current != HOME[HUMAN]) and (current != HOME[COMPUTER]) and \
           (self.pits[current] == 1):
            self.pits[HOME[self.turn]] += 1 + self.pits[12 - current]
            self.pits[current] = self.pits[12 - current] = 0

        # handle second moves
        if (current == HOME[self.turn]) and self.hasMove() and not self.again:
            self.again = True
        else:
            self.again = False
            self.turn  = other(self.turn)
            

    def display(self):
        print
        print ansi.boldBlue() + "      %2d  %2d  %2d  %2d  %2d  %2d" % \
              (self.pits[12], self.pits[11], self.pits[10], \
               self.pits[9],  self.pits[8] , self.pits[7])
        print "  " + ansi.reverse() + ("%2d" % self.pits[13]) \
              + ansi.normal() + "                          " \
              + ansi.boldRed() + ansi.reverse() + ("%2d" % self.pits[6]) \
              + ansi.normal()
        print "      %2d  %2d  %2d  %2d  %2d  %2d" % \
              (self.pits[0], self.pits[1], self.pits[2],
               self.pits[3], self.pits[4], self.pits[5])
        print ansi.reset() + "      " \
              + ansi.reverse() + "#1" + ansi.reverseOff() + "  " \
              + ansi.reverse() + "#2" + ansi.reverseOff() + "  " \
              + ansi.reverse() + "#3" + ansi.reverseOff() + "  " \
              + ansi.reverse() + "#4" + ansi.reverseOff() + "  " \
              + ansi.reverse() + "#5" + ansi.reverseOff() + "  " \
              + ansi.reverse() + "#6" + ansi.reverseOff() + "\n"


    def eval(self):
        if self.gameOver():
            if self.pits[HOME[COMPUTER]] < self.pits[HOME[HUMAN]]:
                return VALUE_LOSE
            elif self.pits[HOME[COMPUTER]] > self.pits[HOME[HUMAN]]:
                return VALUE_WIN
        return self.pits[HOME[COMPUTER]] - self.pits[HOME[HUMAN]]


    def gameOver(self):
        return (self.pits[HOME[HUMAN]] + self.pits[HOME[COMPUTER]]) >= 36


    def hasMove(self):
        for x in range(1, 7):
            if self.pits[HOME[self.turn] - x] > 0:
                return True
        return False

    
    def isLegal(self, move):
        if move < 0:                                return False
        if move == HOME[HUMAN]:                     return False
        if move >= 13:                              return False
        if self.pits[move] == 0:                    return False
        if (self.turn == HUMAN)    and (move > 5):  return False
        if (self.turn == COMPUTER) and (move < 7):  return False
        return True


#------------------------------------------------------------------------

lib.squunkin.hello("Awari", VERSION)
instructions()

done = False
while not done:

    board = Board()
    
    while not board.gameOver():
        if board.hasMove():
            board.display()
            if board.turn == HUMAN:
                board.apply(humanMove(board))
            else:
                board.apply(computerMove(board))
        else:
            board.turn = other(board.turn)

    board.display()
    print ansi.boldWhite() + "\nGAME OVER!"
    if board.pits[HOME[HUMAN]] > board.pits[HOME[COMPUTER]]:
        print "You win!  (By pure luck...)\n"
    elif board.pits[HOME[HUMAN]] < board.pits[HOME[COMPUTER]]:
        print "I win!  (You're only human...)\n"
    else:
        print "Huh, a tie...\n"

    done = (lib.squunkin.input("Another game (y/n)?")[0] != "y")

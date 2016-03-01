from .. import common
from .. import term

VERSION = '0.0.1'

# Whose turn is it?
HUMAN = 0
COMPUTER = 1

# Indices of the "home" pits for each player.
HOME = (6, 13)

# Placeholder value for "no move".
NOWHERE = -1

# Weights for end states in the minimax scoring.
VALUE_LOSE = -100
VALUE_WIN = +100


class Board:
    """Encapsulates the state of the board."""
    
    def __init__(self, *previous):
        # No parameters given: new game. 
        if len(previous) == 0:
            self.pits  = [ 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0 ]
            self.turn  = HUMAN
            self.last  = -1
            self.again = False
            
        # One parameter given: make a copy of this board.
        elif len(previous) == 1:
            self.pits  = list(previous[0].pits)
            self.turn  = previous[0].turn
            self.last  = previous[0].last
            self.again = previous[0].again

        # Two parameters: a board and a move to apply to it.
        else:
            self.pits  = list(previous[0].pits)
            self.turn  = previous[0].turn
            self.again = previous[0].again
            self.Apply(previous[1])
            self.last  = previous[1]

    def Apply(self, move):
        """Execute this move on the current board."""
        
        # Distribute the stones.
        current = move
        while self.pits[move] > 0:
            current = (current + 1) % 14
            self.pits[move]    -= 1
            self.pits[current] += 1

        # Handle captures.
        if (current not in HOME) and (self.pits[current] == 1):
            self.pits[HOME[self.turn]] += 1 + self.pits[12 - current]
            self.pits[current] = self.pits[12 - current] = 0

        # Handle second moves.
        if (current == HOME[self.turn]) and self.HasMove() and not self.again:
            self.again = True
        else:
            self.again = False
            self.turn  = Other(self.turn)

    def Display(self):
        """Dumps the current state to the terminal."""
        term.WriteLn(term.BOLD_BLUE)
        term.WriteLn('      %2d  %2d  %2d  %2d  %2d  %2d' %
                     (self.pits[12], self.pits[11], self.pits[10],
                      self.pits[9],  self.pits[8] , self.pits[7]))
        term.WriteLn('  ', term.REVERSE, ('%2d' % self.pits[13]),
                     term.NORMAL, '                          ', term.BOLD_RED,
                     term.REVERSE, ('%2d' % self.pits[6]), term.NORMAL)
        term.WriteLn('      %2d  %2d  %2d  %2d  %2d  %2d' %
                     (self.pits[0], self.pits[1], self.pits[2],
                      self.pits[3], self.pits[4], self.pits[5]))
        term.WriteLn(term.RESET, '      ',
                     term.REVERSE, '#1', term.NOREVERSE, '  ',
                     term.REVERSE, '#2', term.NOREVERSE, '  ',
                     term.REVERSE, '#3', term.NOREVERSE, '  ',
                     term.REVERSE, '#4', term.NOREVERSE, '  ',
                     term.REVERSE, '#5', term.NOREVERSE, '  ',
                     term.REVERSE, '#6', term.NOREVERSE, '\n')

    def Eval(self):
        """Returns a score for this state, from the computer's perspective."""
        if self.GameOver():
            if self.pits[HOME[COMPUTER]] < self.pits[HOME[HUMAN]]:
                return VALUE_LOSE
            elif self.pits[HOME[COMPUTER]] > self.pits[HOME[HUMAN]]:
                return VALUE_WIN
        return self.pits[HOME[COMPUTER]] - self.pits[HOME[HUMAN]]

    def GameOver(self):
        """Have all of the stones made it into one of the home pits?"""
        return (self.pits[HOME[HUMAN]] + self.pits[HOME[COMPUTER]]) >= 36

    def HasMove(self):
        """Are there any possible moves for the current player?"""
        for x in xrange(1, 7):
            if self.pits[HOME[self.turn] - x] > 0:
                return True
        return False

    def IsLegal(self, move):
        """Is this a legal move under the rules?"""
        return not ((move < 0) or
                    (move == HOME[HUMAN]) or
                    (move >= 13) or
                    (self.pits[move] == 0) or
                    ((self.turn == HUMAN) and (move > 5)) or
                    ((self.turn == COMPUTER) and (move < 7)))


class Move:
    """Used in scoring possible choices."""
    def __init__(self, location, value):
        self.location = location
        self.value    = value


def ComputerMove(board):
    if board.again:
        term.WriteLn(term.BOLD_WHITE, '\nSecond move!')
    else:
        term.WriteLn('My move...')
    move = Minimax(Board(board), 7)
    term.WriteLn(term.BOLD_GREEN, '\nI select the pit opposite #', 13 - move)
    return move
    
def HumanMove(board):
    if board.again:
        term.WriteLn(term.BOLD_WHITE, '\nSecond move!\n')
    move = 0
    while not board.IsLegal(move - 1):
        move = common.InputInt('Your move (1-6)?', 1, 6)
    return move - 1

def MaxMove(board, depth):
    """Maximization phase of the minimax routine."""
    
    # If we're done searching or the game is over, use the current state.
    if (depth == 0) or board.GameOver():
        return Move(board.last, board.Eval())

    # If there's no move, switch sides and try again.
    if not board.HasMove():
        board.turn = Other(board.turn)
        board.again = False
        return MinMove(board, depth)

    # Start with a sentinel move.
    best = Move(NOWHERE, VALUE_LOSE - 1)

    # For each potential move:
    for offset in xrange(1, 7):

        # Make sure it's a legal move.
        location = HOME[board.turn] - offset
        if board.pits[location] == 0:
            continue

        # Calculate its effect on the game state.
        next = Board(board, location)

        # Evaluate that state.
        if next.again:
            move = MaxMove(next, depth - 1)
        else:
            move = MinMove(next, depth - 1)
        if move.value > best.value:
            best = Move(location, move.value)

    # All done!
    return best

def MinMove(board, depth):
    """Minimization phase of the minimax routine."""
    
    # If we're done searching or the game is over, use the current state.
    if (depth == 0) or board.GameOver():
        return Move(board.last, board.Eval())

    # If there's no move, switch sides and try again.
    if not board.HasMove():
        board.turn = Other(board.turn)
        board.again = False
        return MaxMove(board, depth)

    # Start with a sentinel move.
    worst = Move(NOWHERE, VALUE_WIN + 1)

    # For each potential move:
    for offset in xrange(1, 7):

        # Make sure it's a legal move.
        location = HOME[board.turn] - offset
        if board.pits[location] == 0:
            continue

        # Calculate its effect on the game state.
        next = Board(board, location)

        # Evaluate that state.
        if next.again:
            move = MinMove(next, depth - 1)
        else:
            move = MaxMove(next, depth - 1)
        if move.value < worst.value:
            worst = Move(location, move.value)

    # All done!
    return worst

def Minimax(board, depth):
    """Applies minimax to the given depth to seek the best possible move."""
    return MaxMove(board, depth).location

def Other(turn):
    """Returns the constant for the other player's turn."""
    return (turn + 1) % 2

def Instructions():
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
    common.Delay()

#------------------------------------------------------------------------

def Run():
    common.Hello('Awari', VERSION)
    Instructions()

    done = False
    while not done:
        board = Board()
        while not board.GameOver():
            if board.HasMove():
                board.Display()
                if board.turn == HUMAN:
                    board.Apply(HumanMove(board))
                else:
                    board.Apply(ComputerMove(board))
            else:
                board.turn = Other(board.turn)

        board.Display()
        term.WriteLn(term.BOLD_WHITE, '\nGAME OVER!')
        if board.pits[HOME[HUMAN]] > board.pits[HOME[COMPUTER]]:
            term.WriteLn('You win!  (By pure luck...)\n')
        elif board.pits[HOME[HUMAN]] < board.pits[HOME[COMPUTER]]:
            term.WriteLn("I win!  (You're only human...)\n")
        else:
            term.WriteLn('Huh, a tie...\n')

        done = not common.InputYN('Another game (y/n)?')

import random

from .. import common
from .. import term

VERSION = '0.0.1'

# Constants for the current player's turn.
HUMAN    = 0
COMPUTER = 1


def ComputerMove(count, min_take, max_take):
    moves = map(lambda x: [x, (count - x) % (max_take + 1)], range(a, b+1))
    if last_win:
        ok = filter(lambda x: x[1] == 0, moves)
    else:
        ok = filter(lambda x: x[1] == 1, moves)
    if len(ok) > 0:
        return ok[0][0]
    else:
        return random.choice(moves)[0]

def Other(turn):
    return (turn + 1) % 2

def PrintCount(count):
    term.WriteLn(term.RESET)
    if count == 1:
        term.WriteLn('There is ', term.BOLD_GREEN, '1', term.RESET,
                     ' item left.')
    else:
        term.WriteLn('There are ', term.BOLD_GREEN, count, term.RESET,
                     ' items left.')

def Instructions():
    print "This game is a generalization of all the games where you take turns"
    print "taking objects from a pile -- and it allows you to set the rules!"
    print
    print "There's a definite strategy to this class of games, based on modular"
    print "arithmetic... and the computer will follow it, so stay on your toes!"
    print

#------------------------------------------------------------------------

def Run():
    common.Hello('Batnum', VERSION)
    Instructions()

    global a, b, count, last_win, min_take, max_take
    count = common.InputInt('How many objects in the pile (1-100)?', 1, 100)
    last_win = common.InputYN('Win by taking the last object (y/n)?')

    prompt = 'Minimum number to take (1-%d)?' % count
    min_take = common.InputInt(prompt, 1, count)

    prompt = 'Maximum number to take (%d-%d)?' % (min_take, count)
    max_take = common.InputInt(prompt, min_take, count)

    if common.InputYN('Want to go first (y/n)?'):
        turn = COMPUTER
    else:
        turn = HUMAN

    done = False
    while not done:
        current = count
        while current > 0:
            turn = Other(turn)
            a = min(current, min_take)
            b = min(current, max_take)
            PrintCount(current)

            if turn == HUMAN:
                prompt = 'How many do you take (%d-%d)?' % (a, b)
                current -= common.InputInt(prompt, a, b)
            else:
                take = ComputerMove(current, a, b)
                term.WriteLn('The computer takes ', term.BOLD_GREEN, take,
                             term.RESET, '.')
                current -= take

        term.WriteLn()
        if (((turn == HUMAN) and last_win) or
            ((turn == COMPUTER) and not last_win)):
            term.WriteLn(term.BOLD_GREEN, 'You Win!')
        else:
            term.WriteLn(term.BOLD_RED, 'The computer wins!')
        term.WriteLn()

        done = not common.InputYN('Play again (y/n)?')
        term.WriteLn()

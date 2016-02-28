import random

from .. import common
from .. import term

VERSION = '0.0.3'

def CardString(card):
    """Converts a card value (13*suit + number) to a display string."""
    if (card / 13) < 2:
        color = term.BOLD_RED
    else:
        color = term.BOLD_WHITE

    return (color + ('2', '3', '4', '5', '6', '7', '8', '9', '10',
                     'J', 'Q', 'K', 'A')[card % 13]
                  + ('H', 'D', 'S', 'C')[card / 13]
                  + term.RESET)

def ReadBet(cash):
    """Reads in the player's next bet."""
    bet = common.InputInt('How much do you bet?', 1, cash)
    term.Write(term.RESET)
    return bet

def Instructions():
    print "The computer deals two cards face up.  Place your bet according"
    print "to whether you think the next card will be between the first two."
    print
    print "The dealer wins on a tie, aces are high, and you keep playing"
    print "until you're either bored or broke."
    print

def PickCards():
    """Picks the low card, high card, and what the player's going to draw."""
    a = random.randint(0, 51)
    b = random.randint(0, 51)
    c = random.randint(0, 51)
    while (a == b) or (a == c) or (b == c):
        b = random.randint(0, 51)
        c = random.randint(0, 51)
    if Value(a) > Value(b):
        (a, b) = (b, a)
    return (a, b, c)

def ShowCards(a, b):
    term.WriteLn('Here are your cards:  ', CardString(a), '  ', CardString(b))

def ShowCash(cash):
    term.WriteLn('You now have ', term.BOLD_GREEN, '$', cash, term.RESET, '.')

def Value(card):
    return card % 13

#------------------------------------------------------------------------

def Run():
    common.Hello('Acey-Ducey Card Game', VERSION)
    Instructions()

    cash = 100
    while cash > 0:
        (a, b, c) = PickCards()
        ShowCash(cash)
        ShowCards(a, b)
        bet = ReadBet(cash)

        if bet == 0:
            term.WriteLn(term.BOLD_YELLOW, 'Chicken!')
        else:
            term.WriteLn('The next card is: ', CardString(c))
            
        if (Value(a) < Value(c)) and (Value(c) < Value(b)):
            term.WriteLn(term.BOLD_GREEN, 'You win!')
            cash += bet
        else:
            term.WriteLn(term.BOLD_RED, 'Sorry, you lose.')
            cash -= bet

        term.WriteLn(term.RESET)

    term.WriteLn(term.BOLD_WHITE, "You're broke -- get outta here!", term.RESET)

import random

from .. import common
from .. import term

VERSION = '0.0.1'


def CheckBagels(number, guess):
    if ((number.find(guess[0]) == -1) and
        (number.find(guess[1]) == -1) and
        (number.find(guess[2]) == -1)):
        term.Write(term.BOLD_RED, 'BAGELS ')

def CheckFermi(number, guess):
    for i in xrange(3):
        if guess[i] == number[i]:
            term.Write(term.BOLD_GREEN, 'FERMI ')

def CheckPico(number, guess):
    for i in xrange(3):
        if (guess[i] == number[(i+1) % 3]) or (guess[i] == number[(i+2) % 3]):
            term.Write(term.BOLD_YELLOW, 'PICO ')

def Evaluate(number, guess):
    term.WriteLn()
    CheckPico(number, guess)
    CheckFermi(number, guess)
    CheckBagels(number, guess)
    term.WriteLn()

def PickNumber():
    a = random.randint(1, 9)
    b = random.randint(0, 9)
    c = random.randint(0, 9)
    while (a == b) or (a == c) or (b == c):
        b = random.randint(0, 9)
        c = random.randint(0, 9)
    return str(a) + str(b) + str(c)

def ValidGuess(guess):
    s = str(guess)
    result = (s[0] != s[1]) and (s[0] != s[2]) and (s[1] != s[2])
    if not result:
        term.WriteLn(term.BOLD_RED)
        term.WriteLn('As I said, all three digits are different...')
        term.WriteLn()
    return result

def Instructions():
    print "I will think of a number with three digits, all different.  Try to"
    print "guess it!  I'll give you some clue after each guess:"
    print
    print "PICO means that a digit is correct, but in the wrong place."
    print "FERMI means that a digit is correct and in the right place."
    print "BAGELS means that you're entirely wrong!"
    print

#------------------------------------------------------------------------

def Run():
    common.Hello("Bagels", VERSION)
    Instructions()

    prompt = term.BOLD_WHITE + "What's your guess?"

    done = False
    while not done:
        number = PickNumber()
        guess_num = 0
        guess = 0

        while guess != number:
            guess_num += 1
            term.WriteLn(term.BOLD_CYAN)
            term.WriteLn('This is guess #', guess_num)

            guess = str(common.InputInt(prompt, 100, 999))
            while not ValidGuess(guess):
                guess = str(common.InputInt(prompt, 100, 999))

            if number != guess:
                Evaluate(number, guess)

        term.WriteLn(term.BOLD_MAGENTA)
        term.WriteLn('YES!  You got it in ', guess_num, ' guesses!')
        term.WriteLn()

        done = not common.InputYN('Another round (y/n)?')
        term.WriteLn()

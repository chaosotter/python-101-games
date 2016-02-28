import lib.ansi, lib.squunkin, random

ansi    = lib.ansi.Ansi()
VERSION = "0.01"


def checkBagels(number, guess):
    if (number.find(guess[0]) == -1) and \
       (number.find(guess[1]) == -1) and \
       (number.find(guess[2]) == -1):
        print ansi.boldRed() + "BAGELS",

        
def checkFermi(number, guess):
    for i in range(0, 3):
        if guess[i] == number[i]:
            print ansi.boldGreen() + "FERMI",

            
def checkPico(number, guess):
    for i in range(0, 3):
        if (guess[i] == number[(i+1) % 3]) or (guess[i] == number[(i+2) % 3]):
            print ansi.boldYellow() + "PICO",


def evaluate(number, guess):
    print
    checkPico  (number, guess)
    checkFermi (number, guess)
    checkBagels(number, guess)
    print

    
def instructions():
    print "I will think of a number with three digits, all different.  Try to"
    print "guess it!  I'll give you some clue after each guess:"
    print
    print "PICO means that a digit is correct, but in the wrong place."
    print "FERMI means that a digit is correct and in the right place."
    print "BAGELS means that you're entirely wrong!"
    print


def pickNumber():
    a = random.randint(1, 9)
    b = random.randint(0, 9)
    c = random.randint(0, 9)
    while (a == b) or (a == c) or (b == c):
        b = random.randint(0, 9)
        c = random.randint(0, 9)
    return str(a) + str(b) + str(c)


def validGuess(guess):
    s      = str(guess)
    result = (s[0] != s[1]) and (s[0] != s[2]) and (s[1] != s[2])
    if not result:
        print ansi.boldRed() + "\nAs I said, all three digits are different...\n"
    return result


#------------------------------------------------------------------------

lib.squunkin.hello("Bagels", VERSION)
instructions()

prompt = ansi.boldWhite() + "What's your guess?"

done = False
while not done:

    number   = pickNumber()
    guessNum = 0
    guess    = 0

    while guess != number:

        guessNum += 1
        print ansi.boldCyan() + "\nThis is guess #" + str(guessNum)

        guess = str(lib.squunkin.inputNumber(prompt, 100, 999))
        while not validGuess(guess):
            guess = str(lib.squunkin.inputNumber(prompt, 100, 999))

        if number != guess:
            evaluate(number, guess)

    print ansi.boldMagenta() + "\nYES!  You got it in", guessNum, "guesses!\n"
    done = not lib.squunkin.inputYN("Another round (y/n)?")
    print

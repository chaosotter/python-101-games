import lib.ansi, lib.squunkin, random

ansi    = lib.ansi.Ansi()
VERSION = "0.01"

HUMAN    = 0
COMPUTER = 1


def computerMove(count, minTake, maxTake):

    moves = map(lambda x : [x, (count - x) % (maxTake + 1)], range(a, b+1))

    if lastWin:
        okay = filter(lambda x : x[1] == 0, moves)
    else:
        okay = filter(lambda x : x[1] == 1, moves)

    if len(okay) > 0:
        return okay[0][0]
    else:
        return random.choice(moves)[0]

    
def instructions():
    print "This game is a generalization of all the games where you take turns"
    print "taking objects from a pile -- and it allows you to set the rules!"
    print
    print "There's a definite strategy to this class of games, based on modular"
    print "arithmetic... and the computer will follow it, so stay on your toes!"
    print


def other(turn):
    return (turn + 1) % 2


def printCount(count):
    if count == 1:
        print ansi.reset() + "\nThere is "  + ansi.boldGreen() + "1" + \
              ansi.reset() + " item left."
    else:
        print ansi.reset() + "\nThere are " + ansi.boldGreen() + str(count) + \
              ansi.reset() + " items left."

#------------------------------------------------------------------------

lib.squunkin.hello("Batnum", VERSION)
instructions()

count   = lib.squunkin.inputNumber("How many objects in the pile (1-100)?", 1, 100)
lastWin = lib.squunkin.inputYN    ("Win by taking the last object (y/n)?")

prompt  = "Minimum number to take (1-" + str(count) + ")?"
minTake = lib.squunkin.inputNumber(prompt, 1, count)

prompt  = "Maximum number to take (" + str(minTake) + "-" + str(count) + ")?"
maxTake = lib.squunkin.inputNumber(prompt, minTake, count)

if lib.squunkin.inputYN("Want to go first (y/n)?"):
    turn = COMPUTER
else:
    turn = HUMAN

done = False
while not done:

    current = count
    while current > 0:

        turn = other(turn)

        a = min(current, minTake)
        b = min(current, maxTake)
        printCount(current)

        if turn == HUMAN:
            prompt   = "How many do you take (" + str(a) + "-" + str(b) + ")?"
            current -= lib.squunkin.inputNumber(prompt, a, b)
        else:
            take = computerMove(current, a, b)
            print "The computer takes " + ansi.boldGreen() + str(take) + \
                  ansi.reset() + "."
            current -= take

    if ((turn == HUMAN) and lastWin) or ((turn == COMPUTER) and not lastWin):
        print ansi.boldGreen() + "\nYou won!\n"
    else:
        print ansi.boldRed() + "\nThe computer wins!\n"

    done = not lib.squunkin.inputYN("Play again (y/n)?")
    print

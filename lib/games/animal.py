import lib.ansi, lib.squunkin

ansi    = lib.ansi.Ansi()
VERSION = "0.01"


def askQuestion(question):
    answer = ""    
    while (answer != "y") and (answer != "n"):
        answer = lib.squunkin.input(question)
        if answer == 'list':
            print ansi.boldMagenta()
            listAnimals(root)
            print
        elif len(answer) > 1:
            answer = answer[0]
    return answer


def instructions():
    print "Think of an animal, and the computer will try to guess what animal"
    print "you're thinking of.  If it guesses right, hooray for the computer!"
    print "If the computer can't guess it, it will ask you to construct a"
    print "yes-or-no question to help it out the next time."
    print
    print "Enter 'list' for any yes-or-no question to get a list of the"
    print "animals I know."
    print


def listAnimals(current):
    if "a" in current:
        print current["a"]
    else:
        listAnimals(current["y"])
        listAnimals(current["n"])


def newQuestion(old):

    newAnimal = lib.squunkin.input("What was your animal?")
    question  = lib.squunkin.input("Enter a yes-or-no question that would " + \
                                   "distinguish a " + old["a"] + " and a " + \
                                   newAnimal + ":\n")
    answer    = askQuestion("What's the answer for a " + newAnimal + "?")

    old["q"] = question
    if answer == 'y':
        old["y"] = { "a":newAnimal }
        old["n"] = { "a":old["a"]  }
    else:
        old["y"] = { "a":old["a"]  }
        old["n"] = { "a":newAnimal }
    del old["a"]


#------------------------------------------------------------------------

lib.squunkin.hello("Animal Guessing Game", VERSION)
instructions()

root = { "q":"Does it swim?", "y":{"a":"fish"}, "n":{"a":"bird"} }

while True:

    print ansi.boldWhite() + "Time to think of an animal!"
    print ansi.reset()
    current = root

    while "q" in current:
        answer  = askQuestion(current["q"])
        current = current[answer]

    answer = askQuestion("Is it a " + current["a"] + "?")
    if answer == "y":
        print ansi.boldGreen() + "Huzzah!  My powers of deduction win again!\n"
    else:
        print ansi.boldRed() + "Hmmm... I guess I don't know this critter.\n"
        newQuestion(current)

    print

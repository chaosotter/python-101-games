from .. import common
from .. import term

VERSION = '0.0.1'

class Animals:
    """Encapsulates the current tree of questions."""
    
    def __init__(self):
        self.root = {
            'q': 'Does it swim?',
            'y': {'a': 'fish'},
            'n': {'a': 'bird'} }

    def AskQuestion(self, question):
        """Asks the user this question.  Supports 'list' for a status dump."""
        answer = ""
        while answer not in ('y', 'n'):
            answer = common.Input(question)
            if answer == 'list':
                term.Write(term.BOLD_MAGENTA)
                self.List(self.root)
                print
            elif answer:
                answer = answer[0]
        return answer

    def List(self, current):
        """Recursively prints the current list of animals."""
        if 'a' in current:
            print current['a']
        else:
            self.List(current['y'])
            self.List(current['n'])

    def NewQuestion(self, old):
        """Get a question with which to replace the current node."""
        newAnimal = common.Input('What was your animal?')
        question  = common.Input(
            'Enter a yes-or-no question that would distinguish a %s and a %s:\n'
            % (old['a'], newAnimal))
        answer = self.AskQuestion("What's the answer for a %s?" % newAnimal)

        old['q'] = question
        if answer == 'y':
            old['y'] = {'a': newAnimal}
            old['n'] = {'a': old['a']}
        else:
            old['y'] = {'a': old['a']}
            old['n'] = {'a': newAnimal}
        del old['a']

    def Guess(self):
        """Conduct the user through a round of guessing."""
        term.WriteLn()
        term.WriteLn(term.BOLD_WHITE, 'Time to think of an animal!', term.RESET)
        current = self.root

        while 'q' in current:
            answer  = self.AskQuestion(current['q'])
            current = current[answer]

        answer = self.AskQuestion('Is it a %s?' % current['a'])
        if answer == 'y':
            term.WriteLn(term.BOLD_GREEN,
                         'Huzzah!  My powers of deduction win again!')
        else:
            term.WriteLn(term.BOLD_RED,
                         "Hmmm... I guess I don't know this critter.")
            self.NewQuestion(current)
            return


def Instructions():
    print "Think of an animal, and the computer will try to guess what animal"
    print "you're thinking of.  If it guesses right, hooray for the computer!"
    print "If the computer can't guess it, it will ask you to construct a"
    print "yes-or-no question to help it out the next time."
    print
    print "Enter 'list' for any yes-or-no question to get a list of the"
    print "animals I know."
    print

#------------------------------------------------------------------------

def Run():
    common.Hello("Animal Guessing Game", VERSION)
    Instructions()

    animals = Animals()
    while True:
        animals.Guess()

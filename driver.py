import sys

from lib import term
from lib.games import test

term.WriteLn(term.CLEAR, term.Color(term.COLOR_WHITE), term.BOLD)
term.WriteLn('This is ', term.BOLD_RED, 'red', term.BOLD_WHITE, '!')

test.Go()

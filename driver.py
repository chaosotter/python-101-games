import sys

from lib import term

term.WriteLn(term.CLEAR, term.Color(term.COLOR_WHITE), term.BOLD)
term.WriteLn('This is ', term.BOLD_RED, 'red', term.BOLD_WHITE, '!')

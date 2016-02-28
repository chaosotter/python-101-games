"""
Miscellaneous utility functions shared across all games.
"""

import random
import readline

from lib import term

def Delay():
    """Used as a delay instead of the traditional BASIC busy-wait."""
    term.Write(term.RESET, '\n[Press Enter to continue.]')
    raw_input()

def Hello(title, version):
    """Displays a standard welcome banner common to all games."""
    term.Write(term.CLEAR)
    term.WriteLn(term.BOLD_WHITE, title)
    term.WriteLn(term.BOLD_GREEN, 'Inspired by ',
                 term.BOLD_RED, '101 BASIC Computer Games')
    term.WriteLn(term.BOLD_GREEN, 'Python Version ', version, ' by ',
                 term.BOLD_YELLOW, 'Chaosotter')
    term.WriteLn(term.RESET)
    term.WriteLn()
    random.seed()

def Input(prompt):
    """Standard input function; returns user input as a string."""
    return raw_input(term.RESET + prompt + ' ' + term.BOLD_YELLOW)

def InputYN(prompt):
    """Standard yes or no input function; returns a boolean."""
    value = ''
    while value not in ('y', 'n'):
        value = Input(prompt)
        if len(value) > 1:
            value = value[0]
    return (value == 'y')

def InputInt(prompt, min, max):
    """Inputs an integer in the range [min, max] inclusive."""
    value = min - 1
    while (value < min) or (value > max):
        try:
            value = int(Input(prompt))
        except ValueError:
            value = min - 1
    return value

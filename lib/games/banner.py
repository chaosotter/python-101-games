from .. import common
from .. import term

VERSION = '0.0.1'

# Each character is CHAR_X units wide and CHAR_Y units tall.
CHAR_X = 7
CHAR_Y = 9

# Used to assist in centering.
SPACE  = '                                        '

# Bitmap for each character we know.
# Each entry has CHAR_X values and is a bitfield CHAR_Y bits wide.
# We imitate the original code in adding one to each entry for no good reason.
BITMAP = { ' ': (  1,   1,   1,   1,   1,   1,   1),
           'A': (505,  37,  35,  34,  35,  37, 505),
           'G': (125, 131, 258, 258, 290, 163, 101),
           'E': (512, 274, 274, 274, 274, 258, 258),
           'T': (  2,   2,   2, 512,   2,   2,   2),
           'W': (256, 257, 129,  65, 129, 257, 256),
           'L': (512, 257, 257, 257, 257, 257, 257),
           'S': ( 69, 139, 274, 274, 274, 163,  69),
           'O': (125, 131, 258, 258, 258, 131, 125),
           'N': (512,   7,   9,  17,  33, 193, 512),
           'F': (512,  18,  18,  18,  18,   2,   2),
           'K': (512,  17,  17,  41,  69, 131, 258),
           'B': (512, 274, 274, 274, 274, 274, 239),
           'D': (512, 258, 258, 258, 258, 131, 125),
           'H': (512,  17,  17,  17,  17,  17, 512),
           'M': (512,   7,  13,  25,  13,   7, 512),
           '?': (  5,   3,   2, 354,  18,  11,   5),
           'U': (128, 129, 257, 257, 257, 129, 128),
           'R': (512,  18,  18,  50,  82, 146, 271),
           'P': (512,  18,  18,  18,  18,  18,  15),
           'Q': (125, 131, 258, 258, 322, 131, 381),
           'Y': (  8,   9,  17, 481,  17,   9,   8),
           'V': ( 64,  65, 129, 257, 129,  65,  64),
           'X': (388,  69,  41,  17,  41,  69, 388),
           'Z': (386, 322, 290, 274, 266, 262, 260),
           'I': (258, 258, 258, 512, 258, 258, 258),
           'C': (125, 131, 258, 258, 258, 131,  69),
           'J': ( 65, 129, 257, 257, 257, 129, 128),
           '1': (  1,   1, 261, 259, 512, 257, 257),
           '2': (261, 387, 322, 290, 274, 267, 261),
           '*': ( 69,  41,  17, 512,  17,  41,  69),
           '3': ( 66, 130, 258, 274, 266, 150, 100),
           '4': ( 33,  49,  41,  37,  35, 512,  33),
           '5': (160, 274, 274, 274, 274, 274, 226),
           '6': (193, 289, 305, 297, 293, 291, 194),
           '7': (258, 130,  66,  34,  18,  10,   8),
           '8': ( 69, 171, 274, 274, 274, 171,  69),
           '9': (263, 138,  74,  42,  26,  10,   7),
           '=': ( 41,  41,  41,  41,  41,  41,  41),
           '!': (  1,   1,   1, 384,   1,   1,   1),
           '0': ( 57,  69, 131, 258, 131,  69,  57),
           '.': (  1,   1, 129, 449, 129,   1,   1) };

def GetCharacter():
    prompt = 'Enter character to use (leave blank for current character):'
    char = common.Input(prompt)
    if len(char) > 1:
        char = char[0]
    return char

def GetScale(msg, min, max):
    prompt = 'Enter %s scale (%d-%d):' % (msg, min, max)
    return common.InputInt(prompt, min, max)
    
def DrawCharacter(ch):
    tab  = FindTab()
    draw = FindChar(ch)

    for row in xrange(CHAR_Y):
        for y in xrange(scale_y):
            term.Write(SPACE[0:tab])
            for col in xrange(CHAR_X):
                for x in xrange(scale_x):
                    if ((BITMAP[ch][col] - 1) & (1 << row)) != 0:
                        term.Write(draw)
                    else:
                        term.Write(' ')
            term.WriteLn()

    for row in range(scale_y):
        term.WriteLn()

def FindChar(ch):
    if (char == ''):
        return ch
    else:
        return char

def FindTab():
    if centered:
        return (80 - (CHAR_X * scale_x)) / 2
    else:
        return 0

def Instructions():
    print "Enter a message, and I will output it to the screen in large"
    print "block letters.  For extra fun, save the output to a file and"
    print "print it out.  (Or don't, and save a tree!)"
    print

#------------------------------------------------------------------------

def Run():
    common.Hello('Banner', VERSION)
    Instructions()

    global scale_x, scale_y, centered, char, message
    scale_x  = GetScale('horizontal', 1, 11)
    scale_y  = GetScale('vertical', 1, 11)
    centered = common.InputYN('Center output (y/n)?')
    char     = GetCharacter()
    message  = common.Input('Enter message:').upper()

    term.WriteLn(term.BOLD_WHITE)
    for ch in message:
        DrawCharacter(ch)

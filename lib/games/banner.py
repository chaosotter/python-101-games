import lib.ansi, lib.squunkin, sys

ansi    = lib.ansi.Ansi()
VERSION = "0.01"

CHAR_X = 7
CHAR_Y = 9
SPACE  = "                                        "

BITMAP = { " ":[   1,   1,   1,   1,   1,   1,   1 ],
           "A":[ 505,  37,  35,  34,  35,  37, 505 ],
           "G":[ 125, 131, 258, 258, 290, 163, 101 ],
           "E":[ 512, 274, 274, 274, 274, 258, 258 ],
           "T":[   2,   2,   2, 512,   2,   2,   2 ],
           "W":[ 256, 257, 129,  65, 129, 257, 256 ],
           "L":[ 512, 257, 257, 257, 257, 257, 257 ],
           "S":[  69, 139, 274, 274, 274, 163,  69 ],
           "O":[ 125, 131, 258, 258, 258, 131, 125 ],
           "N":[ 512,   7,   9,  17,  33, 193, 512 ],
           "F":[ 512,  18,  18,  18,  18,   2,   2 ],
           "K":[ 512,  17,  17,  41,  69, 131, 258 ],
           "B":[ 512, 274, 274, 274, 274, 274, 239 ],
           "D":[ 512, 258, 258, 258, 258, 131, 125 ],
           "H":[ 512,  17,  17,  17,  17,  17, 512 ],
           "M":[ 512,   7,  13,  25,  13,   7, 512 ],
           "?":[   5,   3,   2, 354,  18,  11,   5 ],
           "U":[ 128, 129, 257, 257, 257, 129, 128 ],
           "R":[ 512,  18,  18,  50,  82, 146, 271 ],
           "P":[ 512,  18,  18,  18,  18,  18,  15 ],
           "Q":[ 125, 131, 258, 258, 322, 131, 381 ],
           "Y":[   8,   9,  17, 481,  17,   9,   8 ],
           "V":[  64,  65, 129, 257, 129,  65,  64 ],
           "X":[ 388,  69,  41,  17,  41,  69, 388 ],
           "Z":[ 386, 322, 290, 274, 266, 262, 260 ],
           "I":[ 258, 258, 258, 512, 258, 258, 258 ],
           "C":[ 125, 131, 258, 258, 258, 131,  69 ],
           "J":[  65, 129, 257, 257, 257, 129, 128 ],
           "1":[   1,   1, 261, 259, 512, 257, 257 ],
           "2":[ 261, 387, 322, 290, 274, 267, 261 ],
           "*":[  69,  41,  17, 512,  17,  41,  69 ],
           "3":[  66, 130, 258, 274, 266, 150, 100 ],
           "4":[  33,  49,  41,  37,  35, 512,  33 ],
           "5":[ 160, 274, 274, 274, 274, 274, 226 ],
           "6":[ 193, 289, 305, 297, 293, 291, 194 ],
           "7":[ 258, 130,  66,  34,  18,  10,   8 ],
           "8":[  69, 171, 274, 274, 274, 171,  69 ],
           "9":[ 263, 138,  74,  42,  26,  10,   7 ],
           "=":[  41,  41,  41,  41,  41,  41,  41 ],
           "!":[   1,   1,   1, 384,   1,   1,   1 ],
           "0":[  57,  69, 131, 258, 131,  69,  57 ],
           ".":[   1,   1, 129, 449, 129,   1,   1 ] };


def instructions():
    print "Enter a message, and I will output it to the screen in large"
    print "block letters.  For extra fun, save the output to a file and"
    print "print it out.  (Or don't, and save a tree!)"
    print


def getCharacter():
    prompt = "Enter character to use (leave blank for current character):"
    char = lib.squunkin.input(prompt)
    if len(char) > 1:
        char = char[0]
    return char


def getScale(msg, min, max):
    prompt = "Enter " + msg + " scale (" + str(min) + "-" + str(max) + "):"
    return lib.squunkin.inputNumber(prompt, min, max)

def drawCharacter(ch):
    
    tab  = findTab()
    draw = findChar(ch)

    for row in range(0, CHAR_Y):
        for y in range(0, scaleY):
            sys.stdout.write(SPACE[0:tab])
            for col in range(0, CHAR_X):
                for x in range(0, scaleX):
                    if ((BITMAP[ch][col] - 1) & (1 << row)) != 0:
                        sys.stdout.write(draw)
                    else:
                        sys.stdout.write(" ")
            sys.stdout.write("\n")

    for row in range(0, scaleY):
        sys.stdout.write("\n")


def findChar(ch):
    if (char == ''):
        return ch
    else:
        return char
    

def findTab():
    if centered:
        return (80 - (CHAR_X * scaleX)) / 2
    else:
        return 0
    

#------------------------------------------------------------------------

lib.squunkin.hello("Banner", VERSION)
instructions()

scaleX   = getScale("horizontal", 1, 11)
scaleY   = getScale("vertical",   1, 11)
centered = lib.squunkin.inputYN("Center output (y/n)?")
char     = getCharacter()
message  = lib.squunkin.input("Enter message:").upper()

print ansi.boldWhite()

for ch in message:
    drawCharacter(ch)

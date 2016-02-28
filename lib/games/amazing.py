import lib.ansi, lib.squunkin, random, readline, sys

ansi    = lib.ansi.Ansi()
VERSION = "0.01"

WALL    = 0
SPACE   = 1
CRUMB   = 2

UP      = 0
DOWN    = 1
LEFT    = 2
RIGHT   = 3

DIR     = [ [-1, 0], [1, 0], [0, -1], [0, 1] ]


def allocateMaze():
    global maze
    maze = []
    for row in xrange(0, rows):
        maze.append([])
        for col in xrange(0, cols):
            maze[row].append(WALL)
    return maze


def canDig(row, col, dir):
    row += 2 * DIR[dir][0]
    col += 2 * DIR[dir][1]
    return (row > 0) and (row < rows) and \
           (col > 0) and (col < cols) and \
           maze[row][col] == WALL


def dig(row, col, dir):
    maze[row                ][col                ] = SPACE
    maze[row +   DIR[dir][0]][col +   DIR[dir][1]] = CRUMB
    maze[row + 2*DIR[dir][0]][col + 2*DIR[dir][1]] = SPACE


def generateMaze():

    row  = 1
    col  = 1
    done = False

    while not done:

        okay = []
        for dir in xrange(0, 4):
            if canDig(row, col, dir):
                okay.append(dir)

        if len(okay) > 0:
            dir = random.choice(okay)
            dig(row, col, dir)
            row += 2 * DIR[dir][0]
            col += 2 * DIR[dir][1]

        elif (row == 1) and (col == 1):
            done = True

        else:
            for dir in range(0, 4):
                if maze[row + DIR[dir][0]][col + DIR[dir][1]] == CRUMB:
                    maze[row + DIR[dir][0]][col + DIR[dir][1]] = SPACE
                    row += 2 * DIR[dir][0]
                    col += 2 * DIR[dir][1]
                    break

    maze[0       ][1       ] = SPACE
    maze[rows - 1][cols - 2] = SPACE
        

def getSize(msg, min, max):
    prompt = "Enter " + msg + " (" + str(min) + "-" + str(max) + "):"
    return lib.squunkin.inputNumber(prompt, min, max)


def instructions():
    print "The computer will generate a maze of the complexity you specify."
    print "There will be only one path through the maze, and an infinite"
    print "variety of mazes can be generated."
    print


def printMaze():
    ansi.clear()
    sys.stdout.write(ansi.boldWhite())

    for row in range(0, rows):
        for col in range(0, cols):
            if maze[row][col] == WALL:
                sys.stdout.write(ansi.reverse())
            else:
                sys.stdout.write(ansi.reverseOff())
            sys.stdout.write(' ')
        sys.stdout.write(ansi.reset() + "\n")


#------------------------------------------------------------------------

lib.squunkin.hello("Amazing Maze Generator", VERSION)
instructions()

cols = getSize("width",  1, 39) * 2 + 1
rows = getSize("height", 1, 39) * 2 + 1

allocateMaze()
generateMaze()
printMaze()

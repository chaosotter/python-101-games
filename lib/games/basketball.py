import lib.ansi, lib.squunkin, random

ansi    = lib.ansi.Ansi()
VERSION = "0.01"

HOME = 0
AWAY = 1

PLAY_30    = 1
PLAY_15    = 2
PLAY_LAYUP = 3
PLAY_SET   = 4

DEFENSE_PRESS      = 1
DEFENSE_MAN_TO_MAN = 2
DEFENSE_ZONE       = 3
DEFENSE_NONE       = 4


def addPoints(which, howMany):
    score[which] += howMany
    printScore()


def awayJump():
    print ansi.boldWhite() + "Jump shot!"
    if (random.random() * 16.0 / (defense + 11)) <= 0.35:
        print ansi.boldBlue() + "Shot is good."
        addPoints(AWAY, 2)
        return HOME
    else:
        return awayJumpMiss()


def awayJumpFoul():
    if (random.random() * 16.0 / (defense + 11)) <= 0.90:
        print "Player fouled.  Two shots."
        doFoul(AWAY)
    else:
        print ansi.boldRed() + "Offensive foul.  IU's ball."
    return HOME


def awayJumpMiss():
    if (random.random() * 16.0 / (defense + 11)) <= 0.75:
        print "Shot is off rim."
        return awayJumpRebound()
    else:
        return awayJumpFoul()


def awayJumpRebound():
    if (random.random() * (defense + 11) / 12.0) <= 0.50:
        print ansi.boldRed() + "IU controls the rebound."
        return HOME
    else:
        print ansi.boldBlue() + opponent + " controls the rebound." + \
              ansi.boldWhite()
        return awayJumpSteal()


def awayJumpSteal():
    if (defense == DEFENSE_PRESS) and (random.random() > 0.75):
        print ansi.boldRed() + "Ball stolen.  Easy lay-up for IU!"
        addPoints(HOME, 2)
        return AWAY
    elif random.random() <= 0.50:
        print "Pass back to " + opponent + " guard."
        return AWAY
    else:
        return awayLayup(PLAY_LAYUP)


def awayLayup(play):
    if play > PLAY_LAYUP:
        print ansi.boldWhite() + "Set shot!"
    else:
        print ansi.boldWhite() + "Lay-up!"
    if (random.random() * 14.0 / (defense + 11)) <= 0.413:
        print ansi.boldBlue() + "Shot is good."
        addPoints(AWAY, 2)
        return HOME
    else:
        return awayLayupMiss()


def awayLayupMiss():
    print "Shot missed."
    return awayJumpRebound()


def checkHalftime(time):
    if time == 50:
        print ansi.boldWhite() + "\n*** END OF FIRST HALF ***"
        printScore()
        raise Exception
    return time


def checkOvertime(time):
    if (time >= 100) and (score[HOME] == score[AWAY]):
        print ansi.boldWhite() + "\n*** END OF SECOND HALF ***"
        printScore()
        print ansi.boldWhite() + "Two-minute overtime!\n"
        time = 93
    return time


def checkWarning(time):
    if time == 92:
        print ansi.boldWhite() + "\nTwo minutes left in the game!\n"
    return time


def doFoul(which):
    if random.random() <= 0.49:
        print "Shooter makes both shots."
        addPoints(which, 2)
    elif random.random() <= 0.75:
        print "Shooter makes one shot and misses one."
        addPoints(which, 1)
    else:
        print "Both shots missed."
        printScore()

        
def getDefense():
    print ansi.boldWhite() + "\nSelect a defense:"
    print ansi.boldYellow() + "  (1) " + ansi.reset() + "Press"
    print ansi.boldYellow() + "  (2) " + ansi.reset() + "Man-to-Man"
    print ansi.boldYellow() + "  (3) " + ansi.reset() + "Zone"
    print ansi.boldYellow() + "  (4) " + ansi.reset() + "None"
    print
    return lib.squunkin.inputNumber("Your choice?", 1, 4)


def getPlay():
    print ansi.boldWhite() + "\nSelect a play:"
    print ansi.boldYellow() + "  (1) " + ansi.reset() + "Long Jump Shot (30')"
    print ansi.boldYellow() + "  (2) " + ansi.reset() + "Short Jump Shot (15')"
    print ansi.boldYellow() + "  (3) " + ansi.reset() + "Lay Up"
    print ansi.boldYellow() + "  (4) " + ansi.reset() + "Set Shot"
    print ansi.boldYellow() + "  (0) " + ansi.reset() + "Change Defense"
    print
    result = lib.squunkin.inputNumber("Your choice?", 0, 4)
    if result == 0:
        defense = getDefense()
        return getPlay()
    print
    return result


def getOpponent():
    print
    return lib.squunkin.input("And who will be your opponent today?")


def homeJump():
    tick()
    print ansi.boldWhite() + "Jump shot!"
    if random.random() <= (0.341 * (defense + 11) / 16.0):
        print ansi.boldRed() + "Shot is good!"
        addPoints(HOME, 2)
        return AWAY
    else:
        return homeJumpMiss()


def homeJumpBlock():
    if random.random() <= (0.782 * (defense + 11) / 16.0):
        print "Shot is blocked!"
        if random.random() <= 0.50:
            print ansi.boldBlue() + "Ball controlled by " + opponent + "."
            return AWAY
        else:
            print ansi.boldRed() + "Ball controlled by IU."
            return HOME
    else:
        return homeJumpFoul()


def homeJumpFoul():
    if random.random() <= (0.843 * (defense + 11) / 16.0):
        print "Shooter is fouled.  Two shots."
        doFoul(HOME)
    else:
        print "Charging foul.  IU loses the ball."
    return AWAY


def homeJumpMiss():
    if random.random() <= (0.682 * (defense + 11) / 16.0):
        print ansi.boldWhite() + "Shot is off-target."
        return homeJumpRebound()
    else:
        return homeJumpBlock()


def homeJumpRebound():
    if ((defense + 11) / 12.0 * random.random()) <= 0.45:
        print ansi.boldBlue() + "Rebound to " + opponent + "..."
        return AWAY
    else:
        print ansi.boldRed() + "IU controls the rebound!" + ansi.boldWhite()
        if random.random() <= 0.40:
            return homeLayup(PLAY_LAYUP)
        else:
            return homeJumpSteal()


def homeJumpSteal():
    if (defense == DEFENSE_PRESS) and (random.random() > 0.6):
        print ansi.boldBlue() + "Pass stolen by " + opponent + " -- easy lay-up!"
        addPoints(AWAY, 2)
    else:
        print "Ball passed back to you."
    return HOME


def homeLayup(play):
    tick()
    if play == PLAY_SET:
        print ansi.boldWhite() + "Set shot!"
    else:
        print ansi.boldWhite() + "Lay-up!"
    if (random.random() * 14.0 / (defense + 11)) <= 0.40:
        print ansi.boldRed() + "Shot is good!  Two points."
        addPoints(HOME, 2)
        return AWAY
    else:
        return homeLayupMiss()


def homeLayupBlock():
    if (random.random() * 14.0 / (defense + 11)) <= 0.925:
        print ansi.boldBlue() + "Shot blocked.  " + opponent + "'s ball."
    else:
        print ansi.boldBlue() + "Charging foul.  IU loses the ball."
    return AWAY


def homeLayupFoul():
    if (random.random() * 14.0 / (defense + 11)) <= 0.875:
        print "Shooter fouled.  Two shots."
        doFoul(HOME)
        return AWAY
    else:
        return homeLayupBlock()


def homeLayupMiss():
    if (random.random() * 14.0 / (defense + 11)) <= 0.70:
        print "Shot is off the rim."
        return homeLayupRebound()
    else:
        return homeLayupFoul()


def homeLayupRebound():
    if random.random() <= 0.66:
        print ansi.boldBlue() + opponent + " controls the rebound."
        return AWAY
    else:
        print ansi.boldRed() + "IU controls the rebound." + ansi.boldWhite()
        if random.random() <= 0.40:
            return homeLayup(PLAY_LAYUP)
        else:
            print "Ball passed back to you."
            return HOME

    
def instructions():
    print "This is a (very loose) simulation of college basketball.  You will"
    print "play the role of Indiana University's team captain and call the plays."
    print
    print "Both teams will always use the same defense.  If you want to change"
    print "your defensive strategy during the game, just select '0' for your shot."
    print


def jumpBall():
    print
    if random.random() <= 0.6:
        print ansi.boldBlue() + opponent + " controls the tap."
        return AWAY
    else:
        print ansi.boldRed() + "IU controls the tap!"
        return HOME


def printScore():
    print ansi.reset()    + "\nScore: ",
    print ansi.boldRed()  + "IU "    +       str(score[HOME]) + " ",
    print ansi.boldBlue() + opponent + " " + str(score[AWAY]) + "\n"


def tick():
    global time
    time += 1
    time = checkHalftime(time)
    time = checkWarning (time)
    time = checkOvertime(time)


#------------------------------------------------------------------------

lib.squunkin.hello("Basketball", VERSION)
instructions()

defense  = getDefense()
opponent = getOpponent()

time     = 0
score    = [ 0, 0 ]

ball = jumpBall()

while time < 100:

    try:
        if ball == HOME:
            print ansi.boldRed() + "IU has the ball." + ansi.reset()
            play = getPlay()
            if (play == PLAY_15) or (play == PLAY_30):
                ball = homeJump()
            else:
                ball = homeLayup(play)
            
        else:
            print ansi.boldBlue() + opponent + " has the ball." + ansi.reset()
            tick()
            play = (2.5 * random.random()) + 1
            if play <= PLAY_30:
                ball = awayJump()
            else:
                ball = awayLayup(play)

    except Exception:
        ball = jumpBall()

print ansi.boldWhite() + "\n*** GAME OVER ***"
printScore()

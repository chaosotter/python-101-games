import random

from .. import common
from .. import term

VERSION = '0.0.1'

# Constants for the current possession.
HOME = 0
AWAY = 1

# Constants for the possible plays.
PLAY_30    = 1
PLAY_15    = 2
PLAY_LAYUP = 3
PLAY_SET   = 4

# Constants for the possible defenses.
DEFENSE_PRESS      = 1
DEFENSE_MAN_TO_MAN = 2
DEFENSE_ZONE       = 3
DEFENSE_NONE       = 4


def AddPoints(which, how_many):
    score[which] += how_many
    PrintScore()

def AwayJump():
    term.WriteLn(term.BOLD_WHITE, 'Jump shot!')
    if (random.random() * 16.0 / (defense + 11)) <= 0.35:
        term.WriteLn(term.BOLD_BLUE, 'Shot is good.')
        AddPoints(AWAY, 2)
        return HOME
    else:
        return AwayJumpMiss()

def AwayJumpFoul():
    if (random.random() * 16.0 / (defense + 11)) <= 0.90:
        term.WriteLn('Player fouled.  Two shots.')
        DoFoul(AWAY)
    else:
        term.WriteLn(term.BOLD_RED, "Offensive foul.  IU's ball.")
    return HOME

def AwayJumpMiss():
    if (random.random() * 16.0 / (defense + 11)) <= 0.75:
        term.WriteLn('Shot is off rim.')
        return AwayJumpRebound()
    else:
        return AwayJumpFoul()

def AwayJumpRebound():
    if (random.random() * (defense + 11) / 12.0) <= 0.50:
        term.WriteLn(term.BOLD_RED, 'IU controls the rebound.')
        return HOME
    else:
        term.WriteLn(term.BOLD_BLUE, opponent, ' controls the rebound.',
                     term.BOLD_WHITE)
        return AwayJumpSteal()

def AwayJumpSteal():
    if (defense == DEFENSE_PRESS) and (random.random() > 0.75):
        term.WriteLn(term.BOLD_RED, 'Ball stolen.  Easy lay-up for IU!')
        AddPoints(HOME, 2)
        return AWAY
    elif random.random() <= 0.50:
        term.WriteLn('Pass back to ', opponent, ' guard.')
        return AWAY
    else:
        return AwayLayup(PLAY_LAYUP)

def AwayLayup(play):
    if play > PLAY_LAYUP:
        term.WriteLn(term.BOLD_WHITE, 'Set shot!')
    else:
        term.WriteLn(term.BOLD_WHITE, 'Lay-up!')
    if (random.random() * 14.0 / (defense + 11)) <= 0.413:
        term.WriteLn(term.BOLD_BLUE, 'Shot is good.')
        AddPoints(AWAY, 2)
        return HOME
    else:
        return AwayLayupMiss()

def AwayLayupMiss():
    term.WriteLn('Shot missed.')
    return AwayJumpRebound()

def CheckHalftime(time):
    if time == 50:
        term.WriteLn(term.BOLD_WHITE)
        term.WriteLn('*** END OF FIRST HALF ***')
        PrintScore()
        raise Exception
    return time

def CheckOvertime(time):
    if (time >= 100) and (score[HOME] == score[AWAY]):
        term.WriteLn(term.BOLD_WHITE)
        term.WriteLn('*** END OF SECOND HALF ***')
        PrintScore()
        term.WriteLn(term.BOLD_WHITE, 'Two-minute overtime!')
        term.WriteLn()
        time = 93
    return time

def CheckWarning(time):
    if time == 92:
        term.WriteLn(term.BOLD_WHITE)
        term.WriteLn('Two minutes left in the game!')
        term.WriteLn()
    return time

def DoFoul(which):
    if random.random() <= 0.49:
        term.WriteLn('Shooter makes both shots.')
        AddPoints(which, 2)
    elif random.random() <= 0.75:
        term.WriteLn('Shooter makes one shot and misses one.')
        AddPoints(which, 1)
    else:
        term.WriteLn('Both shots missed.')
        PrintScore()
        
def GetDefense():
    term.WriteLn(term.BOLD_WHITE)
    term.WriteLn('Select a defense:')
    term.WriteLn(term.BOLD_YELLOW, '  (1) ', term.RESET, 'Press')
    term.WriteLn(term.BOLD_YELLOW, '  (2) ', term.RESET, 'Man-to-Man')
    term.WriteLn(term.BOLD_YELLOW, '  (3) ', term.RESET, 'Zone')
    term.WriteLn(term.BOLD_YELLOW, '  (4) ', term.RESET, 'None')
    term.WriteLn()
    return common.InputInt('Your choice?', 1, 4)

def GetPlay():
    term.WriteLn(term.BOLD_WHITE)
    term.WriteLn('Select a play:')
    term.WriteLn(term.BOLD_YELLOW, '  (1) ', term.RESET, "Long Jump Shot (30')")
    term.WriteLn(term.BOLD_YELLOW, '  (2) ', term.RESET, "Short Jump Shot (15')")
    term.WriteLn(term.BOLD_YELLOW, '  (3) ', term.RESET, 'Lay Up')
    term.WriteLn(term.BOLD_YELLOW, '  (4) ', term.RESET, 'Set Shot')
    term.WriteLn(term.BOLD_YELLOW, '  (0) ', term.RESET, 'Change Defense')
    term.WriteLn()
    result = common.InputInt('Your choice?', 0, 4)
    if result == 0:
        defense = GetDefense()
        return GetPlay()
    term.WriteLn()
    return result

def GetOpponent():
    term.WriteLn()
    return common.Input('And who will be your opponent today?')

def HomeJump():
    Tick()
    term.WriteLn(term.BOLD_WHITE, 'Jump shot!')
    if random.random() <= (0.341 * (defense + 11) / 16.0):
        print term.WriteLn(term.BOLD_RED, 'Shot is good!')
        AddPoints(HOME, 2)
        return AWAY
    else:
        return HomeJumpMiss()

def HomeJumpBlock():
    if random.random() <= (0.782 * (defense + 11) / 16.0):
        term.WriteLn('Shot is blocked!')
        if random.random() <= 0.50:
            term.WriteLn(term.BOLD_BLUE, 'Ball controlled by ', opponent, '.')
            return AWAY
        else:
            term.WriteLn(term.BOLD_RED, 'Ball controlled by IU.')
            return HOME
    else:
        return HomeJumpFoul()

def HomeJumpFoul():
    if random.random() <= (0.843 * (defense + 11) / 16.0):
        term.WriteLn('Shooter is fouled.  Two shots.')
        DoFoul(HOME)
    else:
        term.WriteLn('Charging foul.  IU loses the ball.')
    return AWAY

def HomeJumpMiss():
    if random.random() <= (0.682 * (defense + 11) / 16.0):
        term.WriteLn(term.BOLD_WHITE, 'Shot is off-target.')
        return HomeJumpRebound()
    else:
        return HomeJumpBlock()

def HomeJumpRebound():
    if ((defense + 11) / 12.0 * random.random()) <= 0.45:
        term.WriteLn(term.BOLD_BLUE, 'Rebound to ', opponent, '...')
        return AWAY
    else:
        term.WriteLn(term.BOLD_RED, 'IU controls the rebound!', term.BOLD_WHITE)
        if random.random() <= 0.40:
            return HomeLayup(PLAY_LAYUP)
        else:
            return HomeJumpSteal()

def HomeJumpSteal():
    if (defense == DEFENSE_PRESS) and (random.random() > 0.6):
        term.WriteLn(term.BOLD_BLUE,
                     'Pass stolen by ', opponent, ' -- easy lay-up!')
        AddPoints(AWAY, 2)
    else:
        term.WriteLn('Ball passed back to you.')
    return HOME

def HomeLayup(play):
    Tick()
    if play == PLAY_SET:
        term.WriteLn(term.BOLD_WHITE, 'Set shot!')
    else:
        term.WriteLn(term.BOLD_WHITE, 'Lay-up!')
    if (random.random() * 14.0 / (defense + 11)) <= 0.40:
        term.WriteLn(term.BOLD_RED, 'Shot is good!  Two points.')
        AddPoints(HOME, 2)
        return AWAY
    else:
        return HomeLayupMiss()

def HomeLayupBlock():
    if (random.random() * 14.0 / (defense + 11)) <= 0.925:
        term.WriteLn(term.BOLD_BLUE, 'Shot blocked.  ', opponent, "'s ball.")
    else:
        term.WriteLn(term.BOLD_BLUE, 'Charging foul.  IU loses the ball.')
    return AWAY

def HomeLayupFoul():
    if (random.random() * 14.0 / (defense + 11)) <= 0.875:
        term.WriteLn('Shooter fouled.  Two shots.')
        DoFoul(HOME)
        return AWAY
    else:
        return HomeLayupBlock()

def HomeLayupMiss():
    if (random.random() * 14.0 / (defense + 11)) <= 0.70:
        term.WriteLn('Shot is off the rim.')
        return HomeLayupRebound()
    else:
        return HomeLayupFoul()

def HomeLayupRebound():
    if random.random() <= 0.66:
        term.WriteLn(term.BOLD_BLUE, opponent, ' controls the rebound.')
        return AWAY
    else:
        term.WriteLn(term.BOLD_RED, 'IU controls the rebound.', term.BOLD_WHITE)
        if random.random() <= 0.40:
            return HomeLayup(PLAY_LAYUP)
        else:
            term.WriteLn('Ball passed back to you.')
            return HOME

def JumpBall():
    term.WriteLn()
    if random.random() <= 0.6:
        term.WriteLn(term.BOLD_BLUE, opponent, ' controls the tap.')
        return AWAY
    else:
        term.WriteLn(term.BOLD_RED, 'IU controls the tap!')
        return HOME

def PrintScore():
    term.WriteLn(term.RESET)
    term.Write('Score: ')
    term.Write(term.BOLD_RED, 'IU ', score[HOME], ' ')
    term.WriteLn(term.BOLD_BLUE, opponent, ' ', score[AWAY])

def Tick():
    global time
    time += 1
    time = CheckHalftime(time)
    time = CheckWarning(time)
    time = CheckOvertime(time)

def Instructions():
    print "This is a (very loose) simulation of college basketball.  You will"
    print "play the role of Indiana University's team captain and call the plays."
    print
    print "Both teams will always use the same defense.  If you want to change"
    print "your defensive strategy during the game, just select '0' for your shot."
    print

#------------------------------------------------------------------------

def Run():
    common.Hello('Basketball', VERSION)
    Instructions()

    global defense, opponent, time, score
    defense = GetDefense()
    opponent = GetOpponent()
    time = 0
    score = [ 0, 0 ]

    ball = JumpBall()
    while time < 100:
        try:
            if ball == HOME:
                term.WriteLn(term.BOLD_RED, 'IU has the ball.', term.RESET)
                play = GetPlay()
                if (play == PLAY_15) or (play == PLAY_30):
                    ball = HomeJump()
                else:
                    ball = HomeLayup(play)
            else:
                term.WriteLn(term.BOLD_BLUE, opponent, ' has the ball.', term.RESET)
                Tick()
                play = (2.5 * random.random()) + 1
                if play <= PLAY_30:
                    ball = AwayJump()
                else:
                    ball = AwayLayup(play)
        except Exception:
            ball = JumpBall()

    term.WriteLn(term.BOLD_WHITE)
    term.WriteLn('*** GAME OVER ***')
    PrintScore()

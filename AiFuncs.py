import random
import Player
def getLevelZeroChoice(rerolls, botObj):
    decision = random.randint(0, 1)
    if decision == 0 and rerolls > 0:
        return "reroll"
    else:
        nonLockedScores = []
        for key in botObj.scores.keys():
            if botObj.scores[key][1] == False:
                nonLockedScores.append(key)
        
        return random.choice(nonLockedScores)

            
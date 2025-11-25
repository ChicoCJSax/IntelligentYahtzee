import random
import Player
from collections import Counter

highPriority = ['yahtzee', 'FourOAK', 'fullhse', 'lstr8']
midPriority = [ '4s', '5s', 'ThreeOAK', '6s', 'sstr8']
lowPriority = ['chance', '1s', '2s', '3s']


smallStr8Hands = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]




def getLevelZeroChoice(rerolls, botObj):
    #decision = random.randint(0, 1)
    if rerolls > 0:
        return "reroll"
    else:
        nonLockedScores = []
        for key in botObj.scores.keys():
            if botObj.scores[key][1] == False:
                nonLockedScores.append(key)
        
        return random.choice(nonLockedScores)



def getLevelOneChoice(botObj, rerolls,  currentDice, selectedDice):

    for i in range(0, len(selectedDice)):
        selectedDice[i] = False
        
    for i in range(0, len(highPriority)):
        if(botObj.scores[highPriority[i]][0] > 0 and botObj.scores[highPriority[i]][1] == False):
            print(highPriority[i] + " possible, returning")
            return highPriority[i]

    diceCounts = Counter(currentDice)
    
    for smallset in smallStr8Hands:
        if(rerolls > 0 and smallset.issubset(set(currentDice))):
            print("small straight found! finding dice to keep")
            markedDice = []
            for i in range(0, len(selectedDice)):
                
                if(currentDice[i] not in markedDice and currentDice[i] in smallset):
                    selectedDice[i] = True
                    markedDice.append(currentDice[i])
                
                elif(currentDice[i] in markedDice and currentDice[i] in smallset and selectedDice[i] ==True):
                    selectedDice[i] = False
            return "reroll"
        elif(rerolls == 0 and smallset.issubset(set(currentDice))):
            if(botObj.scores['sstr8'][1]==False):
                return "sstr8"
    

    #go after yahtzee
    if(rerolls > 0 and botObj.scores['yahtzee'][1] == False and 4 in diceCounts.values()):
        for dice, value in diceCounts.items():
            if value == 4:
                diceToKeep = dice
        for i in range(0, len(selectedDice)):
            if(currentDice[i] == diceToKeep):
                selectedDice[i] = True
        return "reroll"
    

    #go after full house
    if(rerolls > 0 and botObj.scores['fullhse'][1] == False and 3 in diceCounts.values()):
        for dice, value in diceCounts.items():
            if value >= 3:
                trioNum = dice
            elif value != 3:
                diceToKeep = dice


        for i in range(0, len(selectedDice)):
            if(currentDice[i] == diceToKeep or currentDice[i] == trioNum):
                selectedDice[i] = True
        return "reroll"
    elif(rerolls == 0 and botObj.scores['ThreeOAK'][1] == False and max(diceCounts.values())>=3):
        print("tried to go after full house, failed, returning ThreeOAK since it is available")
        return "ThreeOAK"
    

    #go after full house 2 (if there's 2 and 2 in values)
    if(rerolls > 0 and botObj.scores['fullhse'][1] == False and 2 in diceCounts.values()):
        
        pairNums = []
        for dice, value in diceCounts.items():
            if value == 2:
                pairNums.append(dice)

        if pairNums == 2:
            for i in range(0, len(selectedDice)):
                if(currentDice[i] == pairNums[0] or currentDice[i] == pairNums[1]):
                    selectedDice[i] = True
                    
            return "reroll"
    elif(rerolls == 0 and botObj.scores['ThreeOAK'][1] == False and max(diceCounts.values())>=3):
        print("tried to go after full house, failed, returning ThreeOAK since it is available")
        return "ThreeOAK"
    

    
    #go after 4 of a kind
    if(rerolls > 0 and botObj.scores['FourOAK'][1] == False and max(diceCounts.values())>=3):
        for dice, value in diceCounts.items():
            if value == 3:
                diceToKeep = dice
        for i in range(0, len(selectedDice)):
            if(currentDice[i] == diceToKeep):
                selectedDice[i] = True
        return "reroll"
    elif(rerolls == 0 and botObj.scores['ThreeOAK'][1] == False and max(diceCounts.values())>=3):
        print("tried to go after four of a kind, failed, returning ThreeOAK since it is available")
        return "ThreeOAK"
    elif(rerolls == 0 and max(diceCounts.values())>=3):
        print("three of a kind not available, returning dice value that is >= 3")
        for diceType, value in diceCounts.items():
            if(value >=3 and botObj.scores[f'{diceType}s'][1] == False):
                return f'{diceType}s'
    
    #pick dice with amount of 2, if hand is junk
    diceToSave = 0
    for dice, value in diceCounts.items():
        if(value == 2 and botObj.scores[f'{dice}s'][1] == False):
            diceToSave = dice
            break
    
    if(diceToSave != 0):
        for i in range(0, len(currentDice)):
            if(currentDice[i] == diceToSave):
                selectedDice[i] == True
        if(rerolls>0):
            return "reroll"
        else:
            return f"{diceToSave}s"

    #out of hands/junk (minimize loss of points)
    defaultHand = None
    if(rerolls>0):
        return "reroll"

    for hand in lowPriority:
        if(botObj.scores[hand][1] == False):
            defaultHand = hand
            return defaultHand
    for hand in midPriority:
        if(botObj.scores[hand][1] == False):
            defaultHand = hand
            return defaultHand
    for hand in highPriority:
        if(botObj.scores[hand][1] == False):
            defaultHand = hand
            return defaultHand


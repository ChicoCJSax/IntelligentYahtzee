import random
import Player
from collections import Counter

highPriority = ['yahtzee', 'lstr8',  'fullhse', 'FourOAK']
midPriority = ['sstr8',"ThreeOAK", "6s", "5s", "4s"]
lowPriority = ['chance',  '3s', '2s', '1s']


smallStr8Hands = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]




def getLevelZeroChoice(rerolls, botObj):
    decision = random.randint(0, 1)
    if rerolls > 0 and botObj.scores['sstr8'][0]>0:
        return "reroll"
    else:
        nonLockedScores = []
        for key in botObj.scores.keys():
            if botObj.scores[key][1] == False:
                nonLockedScores.append(key)
        
        return random.choice(nonLockedScores)



def getLevelOneChoice(botObj, rerolls,  currentDice, selectedDice):
    
    for i in (0, len(selectedDice)):
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
            for i in range(0, 5):
                
                #needs to check if currentdice was already marked:
                #[1, 6, 3, 4, 2]
                #[True, False, True, True, True]
                #small straight found! finding dice to keep
                #[1, 3, 3, 4, 2]
                #[True, True, True, True, True]
                
                if(currentDice[i] not in markedDice and currentDice[i] in smallset):
                    selectedDice[i] = True
                    markedDice.append(currentDice[i])
                
                elif(currentDice[i] in markedDice and currentDice[i] in smallset and selectedDice[i] ==True):
                    selectedDice[i] = False
            print(currentDice)
            print(selectedDice)
            return "reroll"
                
    
    #TEST FOR SELECTING DICE TO KEEP
    #for i in range(0, len(selectedDice)):
    #    selectedDice[i] = not selectedDice[i]            
    

    
    return
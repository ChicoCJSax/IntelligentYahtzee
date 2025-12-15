from collections import Counter
class Player:
    
    def isALargeStraight(dice):
        noDupeDice = []
        for i in dice:
            if i not in noDupeDice:
                noDupeDice.append(i)
        noDupeDice.sort()
        for i in range(min(noDupeDice), max(noDupeDice)):
            if i not in noDupeDice:
                return False
            
        return True
    
    def isASmallStraight(dice):
        numbersets = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
        noDupeDice = set(dice)
        for i in numbersets:
            subsetCheck = i.issubset(noDupeDice)    
            if subsetCheck:       
                return True
            
        return False
                          
    def __init__(self):
        self.scores = {
            "1s": [0, False],
            "2s": [0, False],
            "3s": [0, False],
            "4s": [0, False],
            "5s": [0, False],
            "6s": [0, False],
            "ThreeOAK": [0, False],
            "FourOAK": [0, False],
            "fullhse": [0, False],
            "sstr8": [0, False],
            "lstr8": [0, False],
            "yahtzee": [0, False],
            "chance": [0, False]
            }
  
  
    def calculateBonus(self):
        sumofdice = 0
        for i in range(1,7):
            if(self.scores[f"{i}s"][1]):
                sumofdice += self.scores[f"{i}s"][0]
        return sumofdice
    
    
    def setScore(self, type, scoreVal):
        if self.scores[type][1] == False:
            self.scores[type][0] = scoreVal
  
    def updateScores(self, currentDice):
        dice = Counter(currentDice)     
        for i in range(1, 7):
            self.setScore(f"{i}s", dice[i] * i)

        if max(dice.values()) >= 4:
            self.setScore("FourOAK", sum(currentDice))

        if max(dice.values()) >= 3:
            self.setScore("ThreeOAK", sum(currentDice))
            
        if 3 in dice.values():
            if 2 in dice.values():
                self.setScore("fullhse", 25)

        
        if max(dice) - min(dice) == 4:
            check = Player.isALargeStraight(dice)
            if check == True:
                self.setScore("lstr8", 40)


        if Player.isASmallStraight(dice) == True:
            self.setScore("sstr8", 30)

        if 5 in dice.values():
            self.setScore("yahtzee", 50)

        self.setScore("chance", sum(currentDice))
                        
    def resetValues(self):
        for key, value in self.scores.items():
            if value[1] == False:
                value[0] = 0
                

    def lockScore(self, scoreType):
        self.scores[f"{scoreType}"][1] = True
        
        


            
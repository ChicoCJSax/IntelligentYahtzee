import pygame
import pygame.locals
import random
import sys
import Player
from collections import Counter
import time
import AiFuncs

def rerollDice(dice, selectedDice, freshDice = False):
    if freshDice == True:
        for i in range (0, 5):
            selectedDice[i] = False
            
    for i in range(0, 5):
        if not selectedDice[i]:
            dice[i] = random.randint(1, 6)

def drawPlayerScores(playerObj, key, value, turnCheck = False):
    if not turnCheck: #if not  player's turn, draw only true scores, otherwise draw all 
        if playerObj.scores[key][1] == 1:    
            drawScores(playerObj, key, value)
    else:
        drawScores(playerObj, key, value)

def drawScores(playerObj, key, value):
    textColor = getScoreColor(playerObj.scores[key][1])
    scoreText = scoreFont.render(str(playerObj.scores[key][0]), True, textColor)
    if(len(str(playerObj.scores[key][0])) == 1):
        screen.blit(scoreText, (value[0]+4, value[1]))
    else:
        screen.blit(scoreText, (value[0]-2, value[1]))
    
def getScoreColor(locked):
    color = None
    if locked:
        color = "Black"
    else:
        color = "lightyellow"
    return color

def getBorderColor(selected):
    color = None
    if selected:
        color = "deepskyblue"
    else:
        color = "Black"

    return color        

     
playerScoreCords = {
            "1s": [570, 90],
            "2s": [570, 140],
            "3s": [570, 190],
            "4s": [570, 240],
            "5s": [570, 290],
            "6s": [570, 330],
            "ThreeOAK": [660, 90],
            "FourOAK": [660, 140],
            "fullhse": [660, 190],
            "sstr8": [660, 240],
            "lstr8": [660, 290],
            "yahtzee": [660, 330],
            "chance": [660, 370]
}
botScoreCords = {
            "1s": [605, 90],
            "2s": [605, 140],
            "3s": [605, 190],
            "4s": [605, 240],
            "5s": [605, 290],
            "6s": [605, 330],
            "ThreeOAK": [695, 90],
            "FourOAK": [695, 140],
            "fullhse": [695, 190],
            "sstr8": [695, 240],
            "lstr8": [695, 290],
            "yahtzee": [695, 330],
            "chance": [695, 370]
}



pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

pygame.font.init()
my_font = pygame.font.SysFont('Arial', 80)
scoreFont = pygame.font.SysFont('Calibri', 25)


dice = []
selectedDie = [False] * 5
diceXCords = [80, 321, 562, 803, 1044]
diceYCord = 550


buttonArea = pygame.Rect(340, 430, 600, 100)
for i in range(0, 5):
    dice.append(random.randint(1,6))


player = Player.Player()
bot = Player.Player()
playerScore = 0
botScore = 0
playerBonus = 0
botBonus = 0

rerollNum = 2
playerTurn = True

while running:
    screen.fill("lightgray")
    flag = False #check to see if any score values are unlocked/equal False
    for val in player.scores.values():
        if val[1] == False:
            flag = True

    for val in bot.scores.values():
        if val[1] == False:
            flag = True

    if flag == False:
        print("Your final score is: " +str(playerScore))
        print("The bot's final score is "+str(botScore))
        time.sleep(5)
        running = False
        
    if playerTurn == False:
        botChoice = AiFuncs.getLevelZeroChoice(rerollNum, bot)
        time.sleep(1.5)
        if botChoice == "reroll":
            rerollDice(dice, selectedDie)
            rerollNum -= 1
        else:
            botScore+= bot.scores[botChoice][0]
            bot.lockScore(botChoice)
            rerollDice(dice, selectedDie, freshDice=True)
            rerollNum = 2
            playerTurn = True
                   
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: 
            running = False      
        elif event.type  == pygame.MOUSEBUTTONDOWN and playerTurn == True:
            if event.button == 1:
                if buttonArea.collidepoint(event.pos) and rerollNum > 0:
                    rerollDice(dice, selectedDie)
                    rerollNum -= 1
                for i in range(0, 5):
                    if pygame.Rect(diceXCords[i], diceYCord, 156, 156).collidepoint(event.pos):
                        if not selectedDie[i]:
                            selectedDie[i] = True
                        else:
                            selectedDie[i] = False 
                for key, value in playerScoreCords.items():
                    scoreArea = pygame.Rect(value[0]-5, value[1]-5, 30, 30)
                    if scoreArea.collidepoint(event.pos):
                        if player.scores[key][1] == False:
                            playerScore += player.scores[key][0] 
                            player.lockScore(key)
                            rerollDice(dice, selectedDie, freshDice=True)
                            rerollNum = 2
                            playerTurn = False

    for i in range(0, 5):
        text_surface = my_font.render(str(dice[i]), False, (0, 0, 0))
        screen.blit(text_surface, (diceXCords[i], diceYCord))
        color = getBorderColor(selectedDie[i])
        pygame.draw.rect(screen, color, pygame.Rect(diceXCords[i]-3, diceYCord-3, 162, 162)) 
        diceImg = pygame.image.load("assets/dice" +str(dice[i])+ ".png")
        screen.blit(diceImg, (diceXCords[i], diceYCord))

    rerollDisplay = scoreFont.render("You have " +str(rerollNum)+ " rerolls left", True, (0, 0, 0))
    screen.blit(rerollDisplay, (37, 475))
    
    pygame.draw.rect(screen, 'Black', pygame.Rect(440-4, 10-4, 408, 408)) 
    tableImg = pygame.image.load("assets/table.png")
    screen.blit(tableImg, (440, 10, 400, 400))
    
    pygame.draw.rect(screen, "Black", pygame.Rect(340-3, 430-3, 606, 106))
    pygame.draw.rect(screen, "gray79", buttonArea)

    player.resetValues()
    player.updateScores(dice)
    
    bot.resetValues()
    bot.updateScores(dice)


    for key, value in playerScoreCords.items():
        pygame.draw.rect(screen, "cornflowerblue", pygame.Rect(value[0]-5, value[1]-5, 30, 30))
        drawPlayerScores(player, key, value, turnCheck=playerTurn)


    for key, value in botScoreCords.items():
        pygame.draw.rect(screen, "red", pygame.Rect(value[0]-5, value[1]-5, 30, 30))
        drawPlayerScores(bot, key, value, turnCheck= not playerTurn)


    playerDisplay = scoreFont.render("Your score is "+str(playerScore), True, (0, 0, 0))
    screen.blit(playerDisplay, (37, 200))
    botDisplay = scoreFont.render("The bot's score is "+str(botScore), True, (0, 0, 0))
    screen.blit(botDisplay, (37, 300))

    #bonusText = scoreFont.render(str(playerScore) + "/63", True, (0, 0, 0))
    #screen.blit(bonusText, (572, 380))


    if playerTurn == False:
        turnDisplay = scoreFont.render("It is currently the bot's turn.", True, (0, 0, 0))
    else:
        turnDisplay = scoreFont.render("It is currently your turn.", True, (0, 0, 0))
    screen.blit(turnDisplay, (900, 300))


    buttonText = my_font.render("Click to Reroll", True, (0, 0, 0))
    screen.blit(buttonText, (450, 435)) 

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
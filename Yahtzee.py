import pygame
import pygame.locals
import random
import sys
import Player
from collections import Counter

def rerollDice(dice, selectedDice, freshDice = False):
    if freshDice == True:
        for i in range (0, 5):
            selectedDice[i] = False
            
    for i in range(0, 5):
        if not selectedDice[i]:
            dice[i] = random.randint(1, 6)


def getBorderColor(selected):
    color = None
    if selected:
        color = "deepskyblue"
    else:
        color = "Black"

    return color        

def getTextColor(scoreFlag):
    color = None
    if scoreFlag:
        color = "Black"
    else:
        color = "deepskyblue"

    return color        


player1ScoreCords = {
            "1s": [589, 96],
            "2s": [589, 156],
            "3s": [582, 208],
            "4s": [577, 260],
            "5s": [578, 306],
            "6s": [580, 340],
            "ThreeOAK": [682, 95],
            "FourOAK": [682, 139],
            "fullhse": [675, 183],
            "sstr8": [675, 232],
            "lstr8": [666, 278],
            "yahtzee": [665, 314],
            "chance": [675, 359]
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


player1 = Player.Player()
rerollNum = 2
while running:
    screen.fill("lightgray")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type  == pygame.MOUSEBUTTONDOWN:
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
                for key, value in player1ScoreCords.items():
                    scoreArea = pygame.Rect(value[0]-5, value[1]-5, 35, 35)
                    if scoreArea.collidepoint(event.pos):
                        if player1.scores[key][1] == False:
                            player1.lockScore(key)
                            rerollDice(dice, selectedDie, freshDice=True)
                            rerollNum = 2

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

    player1.resetValues()
    player1.updateScores(dice)

    for key, value in player1ScoreCords.items():
        textColor = getTextColor(player1.scores[key][1])
        scoreText = scoreFont.render(str(player1.scores[key][0]), True, textColor)
        screen.blit(scoreText, (value[0], value[1]))




    buttonText = my_font.render("Click to Reroll", True, (0, 0, 0))
    screen.blit(buttonText, (450, 435)) 



    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
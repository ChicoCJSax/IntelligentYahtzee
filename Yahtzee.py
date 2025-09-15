import pygame
import pygame.locals
import random
import sys


def getBorderColor(selected):
    color = None
    if selected:
        color = "deepskyblue"
    else:
        color = "Black"

    return color        

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


screen.fill("lightgray")

while running:
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
#        elif event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_SPACE:
        elif event.type  == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print(event.pos)
                if buttonArea.collidepoint(event.pos):
                    for i in range(0, 5):
                        if not selectedDie[i]:
                            dice[i] = random.randint(1, 6)
                for i in range(0, 5):
                    if pygame.Rect(diceXCords[i], diceYCord, 156, 156).collidepoint(event.pos):
                        if not selectedDie[i]:
                            selectedDie[i] = True
                        else:
                            selectedDie[i] = False 


    for i in range(0, 5):
        text_surface = my_font.render(str(dice[i]), False, (0, 0, 0))
        screen.blit(text_surface, (diceXCords[i], diceYCord))
        color = getBorderColor(selectedDie[i])
        pygame.draw.rect(screen, color, pygame.Rect(diceXCords[i]-3, diceYCord-3, 162, 162)) 
        diceImg = pygame.image.load("assets/dice" +str(dice[i])+ ".png")
        screen.blit(diceImg, (diceXCords[i], diceYCord))
        


    pygame.draw.rect(screen, 'Black', pygame.Rect(440-4, 10-4, 408, 408)) 
    tableImg = pygame.image.load("assets/table.png")
    screen.blit(tableImg, (440, 10, 400, 400))
    
    pygame.draw.rect(screen, "Black", pygame.Rect(340-3, 430-3, 606, 106))
    pygame.draw.rect(screen, "gray79", buttonArea)


    testScore = scoreFont.render("1", True, (0, 0, 0))
    screen.blit(testScore, (563, 146))

    testScore = scoreFont.render("1", True, (0, 0, 0))
    screen.blit(testScore, (603, 146))


    buttonText = my_font.render("Click to Reroll", True, (0, 0, 0))
    screen.blit(buttonText, (450, 435)) 



    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
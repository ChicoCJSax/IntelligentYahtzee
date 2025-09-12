import pygame
import pygame.locals
import random
import sys


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    buttonCheck = False
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
    my_font = pygame.font.SysFont('Comic Sans MS', 100)


    dice1 = random.randint(1, 6)
    text_surface = my_font.render(str(dice1), False, (0, 0, 0))
    screen.blit(text_surface, (144,0)) #renders text to screen

    


    # flip() the display to put your work on screen
    pygame.display.flip()

    event = pygame.event.wait()

    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()    

    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            continue
    else:
        continue

    clock.tick(60)  # limits FPS to 60

pygame.quit()
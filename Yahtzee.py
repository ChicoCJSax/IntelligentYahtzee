import pygame
import pygame.locals
import random
import sys
import Player
from collections import Counter
import time
import AiFuncs
import firebase_options
import os
import json

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

playerBonusCord = [570, 370]
botBonusCord = [605, 370]


pygame.init()
game = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

pygame.font.init()
my_font = pygame.font.SysFont('Arial', 80)
scoreFont = pygame.font.SysFont('Calibri', 25)
bonusFont = pygame.font.SysFont('Calibri', 15)

titleFont = pygame.font.SysFont('Verdana Bold', 100)
labelFont = pygame.font.SysFont('Arial', 35)


loginFont = pygame.font.SysFont('Arial', 70)
logOutFont = pygame.font.SysFont('Arial', 50)
difficultyFont = pygame.font.SysFont('Arial', 90)


playerInteracted = False
playerScore = 0


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
        game.blit(scoreText, (value[0]+4, value[1]))
    else:
        game.blit(scoreText, (value[0]-2, value[1]))
    
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

def loadUserFromFile():
    hourtime = 3600
    user = None
    if os.path.exists(".userinfo"):
        if (time.time() - os.stat('.userinfo').st_mtime >= hourtime):
            os.remove('.userinfo')
        else:
            with open(".userinfo", 'r') as file:
                user = json.load(file)
    
    return user 

def dumpUser(userObj):
    if userObj!= None:
        with open(".userinfo", 'w') as file:
            json.dump(userObj, file)

def loginPage():

    initialScreen = pygame.display.set_mode((1280, 720))
    loggedIn = False

    emailRect = pygame.Rect(490, 300, 400, 50)
    passwordRect = pygame.Rect(490, 380, 400, 50)
    loginButton = pygame.Rect(600, 470, 150, 75)
    
    email = ""
    password = ""
    errorTrigger = False
    activeBox = None

    try:
        user = loadUserFromFile()
        if(user != None):
            loggedIn = True
    except:
        print("Could not find valid user")

    while not loggedIn:
        initialScreen.fill("lightgray")

        helloText = titleFont.render("Welcome to Intelligent Yahtzee!", True, "black")
        initialScreen.blit(helloText, (120,100))
        pleaseLoginText = labelFont.render("Please sign in below.", True, "black")
        initialScreen.blit(pleaseLoginText, (535,180))

        if(errorTrigger == True):
            errorText = labelFont.render("Error logging in, invalid username or password.", True, "red")
            initialScreen.blit(errorText, (380, 235))



        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if(activeBox == "email"):
                    if(event.key == pygame.K_BACKSPACE and len(email) >= 0):
                        email = email[:-1]
                    else:
                        email += event.unicode
                elif(activeBox == "password"):
                    if(event.key == pygame.K_BACKSPACE and len(password) >= 0):
                        password = password[:-1]
                    else:
                        password += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if emailRect.collidepoint(event.pos):
                        activeBox = "email"
                    elif passwordRect.collidepoint(event.pos):
                        activeBox = "password"
                    else:
                        activeBox = "None"
                    
                    if loginButton.collidepoint(event.pos):
                        try:
                            user = firebase_options.login(email, password)
                        except:
                            print("login failed, invalid info. Attempting signup...")
                            try:
                                user = firebase_options.signup(email, password)
                            except:
                                print("Signup failed")
                                user = None
                                
                        if(user != None):
                            dumpUser(user)
                            loggedIn = True
                        else:
                            print("Error logging in!")
                            errorTrigger = True
                            

        emailLabel = labelFont.render("Email:", True, "black")
        initialScreen.blit(emailLabel, (400, 305))

        passwordLabel = labelFont.render("Password:", True, "black")
        initialScreen.blit(passwordLabel, (345, 385))


        loginOutline = loginButton.inflate(6, 6)
        pygame.draw.rect(initialScreen, "Black", loginOutline)
        pygame.draw.rect(initialScreen, "deepskyblue", loginButton)

        emailOutline = emailRect.inflate(6, 6)
        pygame.draw.rect(initialScreen, "Black", emailOutline)
        pygame.draw.rect(initialScreen, "white", emailRect)

        passwordOutline = passwordRect.inflate(6, 6)
        pygame.draw.rect(initialScreen, "Black", passwordOutline)
        pygame.draw.rect(initialScreen, "white", passwordRect)


        emailDisplay = labelFont.render(email, True, "black")
        initialScreen.blit(emailDisplay, (500, 302))

        passwordDisplay = labelFont.render(password, True, "black")
        initialScreen.blit(passwordDisplay, (500, 382))

        loginText = loginFont.render("Login", True, "white")
        initialScreen.blit(loginText, (606, 460))



        pygame.display.flip()
        clock.tick(60)

    return "mainpage"


def mainPage():
    mainScreenRunning = True
    mainScreen = pygame.display.set_mode((1280, 720))

    easyButton = pygame.Rect(300, 470, 300, 100)
    hardButton = pygame.Rect(680, 470, 300, 100)
    
    logoutButton = pygame.Rect(1105, 25, 150, 55) 
    diceLeft = pygame.Rect(300,  150, 162, 162)
    diceRight = pygame.Rect(900, 150, 162, 162)

    diceLeftNum = random.randint(1, 6)
    diceRightNum = random.randint(1, 6)

    choice = "close"

    while mainScreenRunning:
        mainScreen.fill("lightgray")        
        
        finalText = titleFont.render("Intelligent Yahtzee", True, "Black")
        mainScreen.blit(finalText, (325, 150))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainScreenRunning = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if easyButton.collidepoint(event.pos):
                        choice = "easy"
                        mainScreenRunning = False
                    elif hardButton.collidepoint(event.pos):
                        choice = "hard"
                        mainScreenRunning = False
                    elif logoutButton.collidepoint(event.pos):
                        choice = "login"
                        if os.path.exists(".userinfo"):
                            os.remove(".userinfo")
                        mainScreenRunning = False

        easyOutline = easyButton.inflate(6, 6)           
        pygame.draw.rect(game, "Black", easyOutline)
        pygame.draw.rect(game, "cornflowerblue", easyButton)

        hardOutline = hardButton.inflate(6, 6)           
        pygame.draw.rect(game, "Black", hardOutline)
        pygame.draw.rect(game, "red", hardButton)



        logOutline = logoutButton.inflate(6, 6)           
        pygame.draw.rect(game, "Black", logOutline)
        pygame.draw.rect(game, "red", logoutButton)


        logoutText = logOutFont.render("Log Out", True, "white")
        mainScreen.blit(logoutText, (1106, 20))

        easyText = difficultyFont.render("Level 0", True, "white")
        mainScreen.blit(easyText, (335, 470))

        hardText = difficultyFont.render("Level 1", True, "white")
        mainScreen.blit(hardText, (715, 470))


    
        pygame.display.flip()

        clock.tick(60)

    return choice
    

def gamePage(aiDifficulty):
    global playerInteracted
    global playerScore
    
    dice = []
    selectedDie = [False] * 5
    diceXCords = [80, 321, 562, 803, 1044]
    diceYCord = 550

    buttonArea = pygame.Rect(340, 430, 600, 100)
    for i in range(0, 5):
        dice.append(random.randint(1, 6))

    player = Player.Player()
    bot = Player.Player()
    playerScore = 0
    botScore = 0
    playerBonus = 0
    playerBonusTrigged = False

    botBonus = 0
    botBonusTriggered = False

    rerollNum = 2
    playerTurn = True
    running = True

    wonOrlost = "lost"
    
    while running:
        game.fill("lightgray")
        flag = False  # check to see if any score values are unlocked/equal False
        for val in player.scores.values():
            if val[1] == False:
                flag = True

        for val in bot.scores.values():
            if val[1] == False:
                flag = True

        if flag == False:
            print("Your final score is: " + str(playerScore))
            print("The bot's final score is " + str(botScore))
            if(playerScore>botScore):
                wonOrlost = "won"
            time.sleep(5)
            running = False

        if (playerBonus >= 63 and playerBonusTrigged == False):
            playerScore += 35
            playerBonusTrigged = True

        if (botBonus >= 63 and botBonusTriggered == False):
            botScore += 35
            botBonusTriggered = True

        if playerTurn == False:
            print("ai chosen: " + str(aiDifficulty))
            if(aiDifficulty == "easy"):
                botChoice = AiFuncs.getLevelZeroChoice(rerollNum, bot)
            else:
                botChoice = AiFuncs.getLevelOneChoice(bot, rerollNum, dice, selectedDie)
                
            print(dice)
            print(selectedDie)
            time.sleep(1.5)
            if botChoice == "reroll":
                rerollDice(dice, selectedDie)
                rerollNum -= 1
            else:
                botScore += bot.scores[botChoice][0]
                bot.lockScore(botChoice)
                rerollDice(dice, selectedDie, freshDice=True)
                rerollNum = 2
                playerTurn = True

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and playerTurn == True:
                if event.button == 1:
                    if buttonArea.collidepoint(event.pos) and rerollNum > 0:
                        playerInteracted = True
                        rerollDice(dice, selectedDie)
                        rerollNum -= 1

                    for i in range(0, 5):
                        if pygame.Rect(diceXCords[i], diceYCord, 156, 156).collidepoint(event.pos):
                            selectedDie[i] = not selectedDie[i]

                    for key, value in playerScoreCords.items():
                        scoreArea = pygame.Rect(value[0] - 5, value[1] - 5, 30, 30)
                        if scoreArea.collidepoint(event.pos):
                            
                            playerInteracted = True
                            if player.scores[key][1] == False:
                                playerScore += player.scores[key][0]
                                player.lockScore(key)

                                rerollDice(dice, selectedDie, freshDice=True)
                                rerollNum = 2
                                playerTurn = False

        for i in range(0, 5):
            text_surface = my_font.render(str(dice[i]), False, (0, 0, 0))
            game.blit(text_surface, (diceXCords[i], diceYCord))
            color = getBorderColor(selectedDie[i])
            pygame.draw.rect(game, color, pygame.Rect(diceXCords[i] - 3, diceYCord - 3, 162, 162))
            diceImg = pygame.image.load("assets/dice" + str(dice[i]) + ".png")
            game.blit(diceImg, (diceXCords[i], diceYCord))

        rerollDisplay = scoreFont.render("You have " + str(rerollNum) + " rerolls left", True, (0, 0, 0))
        game.blit(rerollDisplay, (37, 475))

        pygame.draw.rect(game, 'Black', pygame.Rect(440 - 4, 10 - 4, 408, 408))
        tableImg = pygame.image.load("assets/table.png")
        game.blit(tableImg, (440, 10, 400, 400))

        pygame.draw.rect(game, "Black", pygame.Rect(340 - 3, 430 - 3, 606, 106))
        pygame.draw.rect(game, "gray79", buttonArea)

        player.resetValues()
        player.updateScores(dice)

        bot.resetValues()
        bot.updateScores(dice)

        for key, value in playerScoreCords.items():
            pygame.draw.rect(game, "cornflowerblue", pygame.Rect(value[0] - 5, value[1] - 5, 30, 30))
            drawPlayerScores(player, key, value, turnCheck=playerTurn)

        for key, value in botScoreCords.items():
            pygame.draw.rect(game, "red", pygame.Rect(value[0] - 5, value[1] - 5, 30, 30))
            drawPlayerScores(bot, key, value, turnCheck=not playerTurn)

        playerDisplay = scoreFont.render("Your score is " + str(playerScore), True, (0, 0, 0))
        game.blit(playerDisplay, (37, 200))
        botDisplay = scoreFont.render("The bot's score is " + str(botScore), True, (0, 0, 0))
        game.blit(botDisplay, (37, 300))

        # bonus score stuff, red/blue squares and numbers
        pygame.draw.rect(game, "cornflowerblue", pygame.Rect(playerBonusCord[0] - 5, playerBonusCord[1] - 5, 30, 30))
        pygame.draw.rect(game, "red", pygame.Rect(botBonusCord[0] - 5, botBonusCord[1] - 5, 30, 30))

        playerBonus = player.calculateBonus()
        playerbonusTextTop = bonusFont.render(str(playerBonus), True, (0, 0, 0))
        playerbonusTextMiddle = bonusFont.render("___", True, (0, 0, 0))
        playerbonusTextBottom = bonusFont.render("63", True, (0, 0, 0))


        if(len(str(playerBonus)) == 1):
            game.blit(playerbonusTextTop, (577, 366))
        else:
            game.blit(playerbonusTextTop, (573, 366))
            
        game.blit(playerbonusTextMiddle, (569, 366))
        game.blit(playerbonusTextBottom, (573, 380))

        botBonus = bot.calculateBonus()
        botbonusTextTop = bonusFont.render(str(botBonus), True, (0, 0, 0))
        botbonusTextMiddle = bonusFont.render("___", True, (0, 0, 0))
        botbonusTextBottom = bonusFont.render("63", True, (0, 0, 0))

        if(len(str(botBonus)) == 1):
            game.blit(botbonusTextTop, (612, 366))
        else:
            game.blit(botbonusTextTop, (608, 366))

        game.blit(botbonusTextMiddle, (604, 366))
        game.blit(botbonusTextBottom, (608, 380))

        if playerTurn == False:
            turnDisplay = scoreFont.render("It is currently the bot's turn.", True, (0, 0, 0))
        else:
            turnDisplay = scoreFont.render("It is currently your turn.", True, (0, 0, 0))
        game.blit(turnDisplay, (900, 300))

        buttonText = my_font.render("Click to Reroll", True, (0, 0, 0))
        game.blit(buttonText, (450, 435))

        pygame.display.flip()

        clock.tick(60)

    return wonOrlost

def finalScreen(wonOrlost):
    endScreenShow = True
    endScreen = pygame.display.set_mode((1280, 720))
    
    playAgainButton = pygame.Rect(365, 430, 550, 100)


    choice = "close"
    
    user = loadUserFromFile()
    currentUserMax = firebase_options.getMaxScore(user)
    try:
        if currentUserMax<playerScore:
            firebase_options.saveMaxScore(user, playerScore)
            currentUserMax = playerScore
    except:
        print("Error returned, setting with score of 0")
        firebase_options.saveMaxScore(user, 0)
        currentUserMax = playerScore
    if playerInteracted == True:
    
        while endScreenShow:
            endScreen.fill("lightgray")
        
            if(wonOrlost == "won"):
                finalText = titleFont.render("You won!", True, "Black")
    
                endScreen.blit(finalText, (485, 150))
            else:
                finalText = titleFont.render("You lost!", True, "Black")
                endScreen.blit(finalText, (485, 150))
        
            scoreText = scoreFont.render("Your score was " +str(playerScore), True, "Black")
            endScreen.blit(scoreText, (550, 300))
        


            maxScoreText = scoreFont.render("Your highest ever score was " +str(currentUserMax) , True, "Black")
            endScreen.blit(maxScoreText, (475, 350))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endScreenShow = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if playAgainButton.collidepoint(event.pos):
                            choice = "mainpage"
                            endScreenShow = False
                        
            playButtonOutline = playAgainButton.inflate(6, 6)
            pygame.draw.rect(game, "Black", playButtonOutline)
            pygame.draw.rect(game, "deepskyblue", playAgainButton)

            playAgainText = my_font.render("Click to play again", True, "white")
            endScreen.blit(playAgainText, (375, 435))


            pygame.display.flip()

            clock.tick(60)

    return choice




screen = "login"

while(screen != "close"):
    if(screen == "login"):
        screen = loginPage()
    elif(screen == "mainpage"):
        screen = mainPage()
    elif(screen == "easy" or screen == "hard"):
        difficulty = screen
        screen = gamePage(difficulty)
    elif(screen == "won" or screen == "lost"):
        screen = finalScreen(screen)



pygame.quit()
#Arpita Abrol
#Pong game for Raspberry Pi in Python using RPi.GPIO
 
###pins used
#JOYSTICK- SEL: pin 18, GPIO 24
#LEFT: pin 7, GPIO 4 
#RIGHT: pin 32, GPIO 12
#UP: n/a
#DOWN: n/a
 
import pygame, sys
from pygame.locals import *
import RPi.GPIO as GPIO
import time, random, csv, itertools, os
 
#Frames per second
global FPS
FPS = 100
 
#Global Variables
WIDTH = 400
HEIGHT = 300
THICK = 10
PADDLESIZE = 50
PADDLEOFF = 20
##input vars
LEFT = 7     #pin 7
RIGHT = 32   #pin 32
SEL = 36     #pin 18
##colors
BLACK = (0,0,0)
WHITE = (255,255,255)
 
 
 
 
#Methods
 
#sets up the GPIO controls for the game
def GPIOsetup():
    #GPIO SETUP
    GPIO.setmode(GPIO.BOARD)     #Numbers GPIOs by physical location aka pin num
    GPIO.setup(LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
#sets up the game background
def setup():
    #BACKGROUND SETUP
    DISPLAYSURF.fill(BLACK)
    pygame.draw.rect(DISPLAYSURF,WHITE,((0,0),(WIDTH,HEIGHT)),THICK*2)
    pygame.draw.line(DISPLAYSURF,WHITE,((WIDTH/2),0),((WIDTH/2),HEIGHT),THICK/4)
 
#draws the paddles and ensure they stay within game limits
def drawPaddle(paddle):
    if paddle.bottom > HEIGHT - THICK:
        paddle.bottom = HEIGHT - THICK
    elif paddle.top < THICK:
        paddle.top = THICK
    pygame.draw.rect(DISPLAYSURF,WHITE,paddle)
 
#draws the ball
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF,WHITE,ball)
 
#moves the ball
def moveBall(ball,Xdir,Ydir):
    ball.x += Xdir
    ball.y += Ydir
    return ball
 
#checks if the ball collides with top, bottom, paddles
def checkEdges(ball, Xdir, Ydir, score, topScore,FPS):
    if ball.top <= THICK or ball.bottom >= HEIGHT-THICK:
        Ydir *= -1
    if ball.left <= THICK or ball.right >= WIDTH-THICK:
        FPS = 100
        if ball.right >= WIDTH-THICK-2:
            score += 10
        else:
            score = 0
        if Xdir < 0:
            Xdir = 1
        else:
            Xdir = -1
        ball.y = HEIGHT/2
        ball.x = WIDTH/2 + 20*Xdir*-1
        if score > topScore:
            topScore = score
        score = 0
    return ball, Xdir, Ydir, score, topScore, FPS
 
#moves the opponent's paddle
def AI(ball, Xdir, paddle):
    if Xdir < 0 and random.random() >= .5:
        if paddle.centery < HEIGHT/2:
            paddle.y += 1
        elif paddle.centery > HEIGHT/2:
            paddle.y += -1
    elif Xdir > 0:
        if paddle.centery < ball.centery:
            paddle.y += 1
        elif paddle.centery > ball.centery:
            paddle.y += -1
    return paddle
 
#checks if paddle hits ball
def checkPaddles(ball,paddleOne,paddleTwo,Xdir, FPS):
    if Xdir < 0 and paddleOne.right == ball.left and paddleOne.top-7 <= ball.bottom and paddleOne.bottom+7 >= ball.top:
        FPS += 2
        return Xdir * -1, FPS
    elif Xdir > 0 and paddleTwo.left == ball.right and paddleTwo.top-7 <= ball.bottom and paddleTwo.bottom+7 >= ball.top:
        FPS += 2
        return Xdir * -1, FPS
    else:
        return Xdir, FPS
 
#checks if score increased or now zero
def checkScore(paddle,ball,score,Xdir):
    if Xdir < 0 and paddle.right == ball.left and paddle.top-7 <= ball.bottom and paddle.bottom+7 >= ball.top:
        return score + 1
    elif ball.right >= WIDTH-THICK:
        return score + 10
    return score
 
#displays current score
def displayScore(score):
    res = FONT.render('Score = %s' %(score),True,WHITE)
    resRect = res.get_rect()
    resRect.topleft = (WIDTH - 150, 25)
    DISPLAYSURF.blit(res,resRect)
 
 
 
 
#leaderboard function (endgame); main 2.0
def scoreboard(score):
    with open('highscores.csv','rb') as file:
        words = csv.reader(file)
        score_list = list(words)
        lnOne = score_list[0][0].split('.')
         
    pos,newHigh = compareScores(score,lnOne)
    if( newHigh ):
        name = getName()
        replaceScores(name,pos,score)
    else:
        finalScreen()
 
#Compares the player score to all high scores
def compareScores(newScore,listScores):
    x = 0
    while x < len(listScores):
        if int(newScore) >= int(listScores[x]):
            return x, True
        x += 1
    return -1, False
 
#get player name
def getName():
    pygame.time.wait(500)
    DISPLAYSURF.fill(BLACK)
    name = ""
    alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    check = True
    x1 = 0
    while check:
        DISPLAYSURF.fill(BLACK)
        displayBoard('WHAT IS YOUR FIRST INITIAL?',2)
        displayName(alphabet[x1],50)
        if not GPIO.input(SEL):
            name += alphabet[x1]
            check = False
        if not GPIO.input(RIGHT):
        #if GPIO.add_event_detect(RIGHT, GPIO.FALLING):
            x1 += 1
            if x1 >= 26:
                x1 = 0
        if not GPIO.input(LEFT):
        #if GPIO.add_event_detect(LEFT, GPIO.FALLING):
            x1 -= 1
            if x1 <= -1:
                x1 = 25
        pygame.time.wait(200)
        pygame.display.update()
 
    pygame.time.wait(300)
     
    check = True
    x1 = 0
    while check:
        DISPLAYSURF.fill(BLACK)
        displayBoard('WHAT IS YOUR LAST INITIAL?',2)
        displayName(alphabet[x1],50)
        if not GPIO.input(SEL):
            name += alphabet[x1]
            check = False
        if not GPIO.input(RIGHT):
            x1 += 1
            if x1 >= 26:
                x1 = 0
        if not GPIO.input(LEFT):
            x1 -= 1
            if x1 <= -1:
                x1 = 25
        pygame.time.wait(200)
        pygame.display.update()
         
    return name
 
#displays name choosing stuff
def displayName(words,pos):
    res = FONT2.render('%s' %words,True,WHITE)
    resRect = res.get_rect()
    resRect.topleft = (25,pos)
    DISPLAYSURF.blit(res,resRect)
 
#replaces the old high score
def replaceScores(name,pos,score):
    #print name,pos,score
    #name -> new name
    #pos -> new pos
    #score -> new score
 
    score_list = []
     
    with open('highscores.csv','rb') as file:
        words = csv.reader(file)
        score_list = list(words)
         
    with open('highscores.csv','wb') as file:
        lnOne = score_list[0][0].split('.')
        ctr = 9
        while ctr > pos:
            lnOne[ctr] = lnOne[ctr-1]
            ctr -= 1
        lnOne[pos] = str(score)
        string = ""
        for x in lnOne:
            string += x
            string += "."
        file.write(string[0:-1] + '\n')
        ctr = 1
        while ctr < pos+2:
            file.write(score_list[ctr][0])
            file.write('\n')
            ctr += 1
        if pos < 9:
            string = "0" + str(pos+1) + "." + "            " + name + "            " + str(score) + "\n"
            file.write(string)
            ctr = pos+2
            while ctr < 10:
                string = score_list[ctr][0]
                num = int(string[:2]) + 1
                string = "0" + str(num) + string[2:]
                file.write(string)
                file.write('\n')
                ctr += 1
            string = score_list[10][0]
            string = "10" + string[2:]
            file.write(string)
        else:
            string = "10." + "            " + name + "            " + str(score) + "\n"
            file.write(string)
    finalScreen()
 
def finalScreen():
    DISPLAYSURF.fill(BLACK)
    ctr = 1
    with open('highscores.csv','rb') as file:
        words = csv.reader(file)
        score_list = list(words)
        for x in score_list:
            displayBoard(x[0],ctr)
            ctr += 1
        lnOne = score_list[0][0].split('.')
     
    pygame.display.update()
    pygame.time.wait(10000)
    pygame.quit()
    sys.exit()
 
def displayBoard(words,pos):
    #print words
    res = FONT2.render('%s' %words,True,WHITE)
    resRect = res.get_rect()
    resRect.topleft = (25,pos*20-37)
    DISPLAYSURF.blit(res,resRect)
 
 
 
 
def main():
    #basic setup stuff
    global FPS
    FPS = 100
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Robo Pong')
 
    #font info
    global FONT, FONT2
    FONT = pygame.font.Font('freesansbold.ttf',20)
    FONT2 = pygame.font.Font('incon.ttf',15)
    GPIOsetup()
 
    #setup starting pos
    ballX = (WIDTH - THICK)/2
    ballY = (HEIGHT - THICK)/2
    playerOnePos = (HEIGHT - PADDLESIZE)/2
    playerTwoPos = (HEIGHT - PADDLESIZE)/2
 
    #setup paddles, ball
    paddleOne = pygame.Rect(PADDLEOFF,playerOnePos,THICK,PADDLESIZE)
    paddleTwo = pygame.Rect(WIDTH-PADDLEOFF-THICK,playerTwoPos,THICK,PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, THICK, THICK)
 
    #place paddles, ball initially
    setup()                 #draws background
    drawPaddle(paddleOne)   #draws user's paddle
    drawPaddle(paddleTwo)   #draws AI's paddle
    drawBall(ball)          #draws ball
 
    #ball directions:
    ##X-axis: -1 = left, 1 = right
    ##Y-axis: -1 = up, 1 = down
    ballDirX = -1
    ballDirY = -1
         
    score = 0
    topScore = 0
    while True:     #PONG game loop
        """for action in pygame.event.get():
            if action.type == KEYDOWN:
                if (not PRESS_S):     #if select button pressed, initiate quit
                    pygame.quit()    #later: add high score screen
                    sys.exit()"""
        if not GPIO.input(SEL):
            if topScore > score:
                scoreboard(topScore)
            else:
                scoreboard(score)
        if not GPIO.input(LEFT):
            paddleOne.y += -2
        if not GPIO.input(RIGHT):
            paddleOne.y += 2
             
        #place paddles, ball- updating version
        setup()                 #draws background
        drawPaddle(paddleOne)   #draws user's paddle
        drawPaddle(paddleTwo)   #draws AI's paddle
        drawBall(ball)          #draws ball
 
        ball = moveBall(ball,ballDirX,ballDirY)
        ball, ballDirX, ballDirY, score, topScore, FPS = checkEdges(ball,ballDirX,ballDirY,score,topScore,FPS)
        score = checkScore(paddleOne,ball,score,ballDirX)
        ballDirX,FPS = checkPaddles(ball,paddleOne,paddleTwo,ballDirX,FPS)
        paddle2 = AI(ball,ballDirX,paddleTwo)
        displayScore(score)
                     
        pygame.display.update()
        FPSCLOCK.tick(FPS)
 
 
if __name__ == '__main__':
    main()
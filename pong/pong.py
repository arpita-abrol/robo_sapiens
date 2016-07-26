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
import time
import random

#Frames per second
FPS = 200

#Global Variables
WIDTH = 400
HEIGHT = 300
THICK = 10
PADDLESIZE = 50
PADDLEOFF = 20
##input vars
LEFT = 7     #pin 7
RIGHT = 32   #pin 32
SEL = 18     #pin 18

# Note: gotta make another var for each and do selL = GPIO.input(7).
#       False means pressed, True -> not pressed

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
    global PRESS_L
    PRESS_L = GPIO.input(7)
    global PRESS_R
    PRESS_R = GPIO.input(32)
    global PRESS_S
    PRESS_S = GPIO.input(18)

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

def main():
    #basic setup stuff
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Robo Pong')

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
    
    while True:     #PONG game loop
        for action in pygame.event.get():
            if action.type == KEYDOWN:
                if (not PRESS_S):     #if select button pressed, initiate quit
                    pygame.quit()    #later: add high score screen
                    sys.exit()
        if not PRESS_S:
            pygame.quit()
            sys.exit()

        #place paddles, ball- updating version
        setup()                 #draws background
        drawPaddle(paddleOne)   #draws user's paddle
        drawPaddle(paddleTwo)   #draws AI's paddle
        drawBall(ball)          #draws ball
                    
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()

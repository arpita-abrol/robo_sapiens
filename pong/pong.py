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
PADDLESIDE = 50
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

#sets up the window for the game
def setup():
    #GPIO SETUP
    GPIO.setmode(GPIO.BOARD)     #Numbers GPIOs by physical location aka pin num
    GPIO.setup(LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    global PRESSL
    pressL = GPIO.input(7)
    global PRESSR
    pressR = GPIO.input(32)
    global PRESSS
    pressS = GPIO.input(18)
    #BACKGROUND SETUP
    DISPLAYSURF.fill(BLACK)
    pygame.draw.rect(DISPLAYSURF,WHITE,((0,0),(WIDTH,HEIGHT)),20)


def main():
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Robo Pong')

    setup()
    
    while True:     #PONG game loop
        for action in pygame.event.get():
            if action.type == KEYDOWN:
                if (not PRESSS):     #if select button pressed, initiate quit
                    pygame.quit()    #later: add high score screen
                    sys.exit()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()

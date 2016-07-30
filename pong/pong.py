#Arpita Abrol
#Pong game for Raspberry Pi in Python using RPi.GPIO

###pins used
#LEFT: GPIO 
#RIGHT:
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

#GPIO SETUP
GPIO.setmode(GPIO.BCM)
#GPIO.setup()
# Args: setup(channel #, input/output)
# More info here: https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

#Methods

#sets up the window for the game
def setup():
    background.fill(0,75,150)


setup()

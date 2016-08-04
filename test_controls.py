#Arpita Abrol
#Systems Test for the Raspberry Pi 2 Game Console
#see overview.txt for all pin positions

import RPi.GPIO as GPIO
import pygame, sys
from pygame import *

#GLobal Variables
##buttons
LEFT = 7     #pin 7
RIGHT = 32   #pin 32
UP = 36      #pin 36
DOWN = 37    #pin 37
##joystick
HOR = 12     #pin 12
VER = 16     #pin 16
SEL = 18     #pin 18

GPIO.setmode(GPIO.BOARD)

GPIO.setup(LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()

def loop():
    print 'hi'
    while True:
        if( not GPIO.input(7) ):
            print 'LEFT BUTTON PRESSED'
        if( not GPIO.input(32) ):
            print 'RIGHT BUTTON PRESSED'
        if( not GPIO.input(36) ):
            print 'UP BUTTON PRESSED'
        if( not GPIO.input(37) ):
            print 'DOWN BUTTON PRESSED'
        if( not GPIO.input(18) ):
            print 'SEL BUTTON PRESSED'

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt: #Ctrl + C
        destroy()
    
    

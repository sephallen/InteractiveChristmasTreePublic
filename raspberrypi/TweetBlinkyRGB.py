#!/usr/bin/env python

import os
import sys
import pygame
import pygame.camera
from pygame.locals import *
import time
import threading
import RPi.GPIO as GPIO
from twython import TwythonStreamer
from twython import Twython
import random

# Initialise Webcam
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(640,480))

# Search terms
TERMS = '@thinkingjuice,@weareemerge,@sephallen,@tjxmaspi,@ben_poulson,@dj10dj100'

# GPIO pin number of LED
RED = 22
GREEN = 16
BLUE = 18

# Twitter application authentication
APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

def ledFlash():
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.HIGH)
        time.sleep(0.5)
        return

def ledRed():
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW)
        GPIO.output(RED, GPIO.HIGH)
        return

def ledGreen():
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.LOW)
        GPIO.output(RED, GPIO.LOW)
        return

def ledBlue():
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.HIGH)
        GPIO.output(RED, GPIO.LOW)
        return

def ledWhite():
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.HIGH)
        GPIO.output(RED, GPIO.HIGH)
        return

def ledYellow():
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.LOW)
        GPIO.output(RED, GPIO.HIGH)
        return

def ledPink():
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.HIGH)
        GPIO.output(RED, GPIO.HIGH)
        return

def ledCyan():
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.HIGH)
        GPIO.output(RED, GPIO.LOW)
        return

def lightShow():
        ledRed()
        time.sleep(1)
        ledGreen()
        time.sleep(1)
        ledBlue()
        time.sleep(1)
        ledWhite()
        time.sleep(1)
        ledYellow()
        time.sleep(1)
        ledPink()
        time.sleep(1)
        ledCyan()
        time.sleep(1)
        return

def jingleBells():
        os.system("mpg123 mp3/jinglebells.mp3")
        return

def weWishYou():
        os.system("mpg123 mp3/wewishyou.mp3")
        return

def littleDonkey():
        os.system("mpg123 mp3/littledonkey.mp3")
        return

def ohChristmasTree():
        os.system("mpg123 mp3/ohchristmastree.mp3")
        return

def deckTheHalls():
        os.system("mpg123 mp3/deckthehalls.mp3")
        return

def drivingHome():
        os.system("mpg123 mp3/drivinghomeforchristmas.mp3")
        return

def takePhoto():
        time.sleep(random.randint(0,30))
        cam.start()
        image = cam.get_image()
        pygame.image.save(image,'webcam.jpg')
        photo = open('webcam.jpg','rb')
        api = Twython(APP_KEY,APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
        api.update_status_with_media(media=photo, status='@tjxmaspi #devteam')
	cam.stop()

# Setup callbacks from Twython Streamer
class BlinkyStreamer(TwythonStreamer):
        def on_success(self, data):
                if 'text' in data:
                        TWEET = data['text'].encode('utf-8')
                        print TWEET
                        print
                        if '#one' in TWEET:
                                FLASH = 1
                                for i in range(FLASH):
                                        ledFlash()
			elif '#two' in TWEET:
				FLASH = 2
                                for i in range(FLASH):
                                        ledFlash()
			elif '#three' in TWEET:
				FLASH = 3
                                for i in range(FLASH):
                                        ledFlash()
			elif '#four' in TWEET:
				FLASH = 4
                                for i in range(FLASH):
                                        ledFlash()
                        elif '#red' in TWEET:
                                ledRed()
                        elif '#green' in TWEET:
                                ledGreen()
                        elif '#blue' in TWEET:
                                ledBlue()
                        elif '#white' in TWEET:
                                ledWhite()
                        elif '#yellow' in TWEET:
                                ledYellow()
                        elif '#pink' in TWEET:
                                ledPink()
                        elif '#cyan' in TWEET:
                                ledCyan()
                        elif '#jinglebells' in TWEET:
                                threading.Thread(target = jingleBells).start()
                                REPEATLIGHTS = 15
                                for i in range(REPEATLIGHTS):
                                        lightShow()
                        elif '#wewishyouamerrychristmas' in TWEET:
                                threading.Thread(target = weWishYou).start()
                                REPEATLIGHTS = 20
                                for i in range(REPEATLIGHTS):
                                        lightShow()
                        elif '#littledonkey' in TWEET:
                                threading.Thread(target = littleDonkey).start()
                                REPEATLIGHTS = 12
                                for i in range(REPEATLIGHTS):
                                        lightShow()
                        elif '#ohchristmastree' in TWEET:
                                threading.Thread(target = ohChristmasTree).start()
                                REPEATLIGHTS = 7
                                for i in range(REPEATLIGHTS):
                                        lightShow()
                        elif '#deckthehalls' in TWEET:
                                threading.Thread(target = deckTheHalls).start()
                                REPEATLIGHTS = 16
                                for i in range(REPEATLIGHTS):
                                        lightShow()
                        elif '#drivinghomeforchristmas' in TWEET:
                                threading.Thread(target = drivingHome).start()
                                REPEATLIGHTS = 37
                                for i in range(REPEATLIGHTS):
                                        lightShow()
                        elif '#cheese' in TWEET:
                                takePhoto()
                        else:
                                FLASH = 5
                                for i in range(FLASH):
                                        ledFlash()


# Setup GPIO as output
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RED, GPIO.OUT)
GPIO.output(RED, GPIO.LOW)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.output(GREEN, GPIO.LOW)
GPIO.setup(BLUE, GPIO.OUT)
GPIO.output(BLUE, GPIO.LOW)

# Create streamer
try:
        stream = BlinkyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
        GPIO.cleanup()

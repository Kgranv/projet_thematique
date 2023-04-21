import os
import sys
import numpy as np
import pandas as pd
import RPi.GPIO as GPIO

dataFolder = "data"
dataPath = "./"+dataFolder+"/"

def checkFolder(folder):
    """
    Check if folder exist if not create it.
    return true if exist, if not return false
    """
    if not os.path.isdir(folder):
        print(dataFolder, "folder was not found. Run dataPreparation.py to prepare your data.")
        sys.exit(0)
    else:
        pass

class pinGPIO:
    """
    Setup GPIO lib
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)


'''
servo_pin = 18  # équivalent de GPIO 18
GPIO.setmode(GPIO.BCM)  # notation BCM
GPIO.setup(servo_pin, GPIO.OUT)  # pin configurée en sortie
pwm = GPIO.PWM(servo_pin, 50)  # pwm à une fréquence de 50 Hz
rapport = 7       # rapport cyclique initial de 7%
pwm.start(rapport)
pwm.ChangeDutyCycle(float(rapport))
'''

checkFolder(dataFolder)
setupGPIO()

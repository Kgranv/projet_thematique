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

def setupPWM(pinMotor:list,pinVanne:list):
    """
    Setup GPIO PWM with a frequency of 10Hz
    """
    frequencyPWM = 10
    moteur = [GPIO.PWM(pinMotor[0],frequencyPWM),GPIO.PWM(pinMotor[1],frequencyPWM),GPIO.PWM(pinMotor[2],frequencyPWM)]
    vanne = [GPIO.output(pinVanne[0],GPIO.HIGH),GPIO.output(pinVanne[1],GPIO.HIGH),GPIO.output(pinVanne[2],GPIO.HIGH)]
    return moteur,vanne

def setupGPIO():
    """
    Setup GPIO for control
    """
    #Pompe
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    #Electrovanne
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)

def testPWM(isMotor:bool,index:int,dutyCycle:float):
    """
    DO NOT USE ! FOR DEBUG ONLY !
    index : 0,1 or 2
    dutyCycle : 0.0<dc<100.0
    """
    if isMotor:
        motor[index].start(dutyCycle)
        input('Press return to stop:')   # use raw_input for Python 2
        motor[index].stop()
    else:
        vanne[index].start(dutyCycle)
        input('Press return to stop:')   # use raw_input for Python 2
        vanne[index].stop()

def endProgram():
    """
    Clean all GPIO used for clean ending
    """
    GPIO.cleanup()
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
motor,vanne = setupPWM([17,27,22],[5,6,13])
for i in range(0,3):
    testPWM(True,i,50)
for i in range(0,3):
    testPWM(False,i,50)
endProgram()
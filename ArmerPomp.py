import RPi.GPIO as GPIO
import time

def setupGPIO():
    """
    Setup GPIO for control
    """
    GPIO.setmode(GPIO.BCM)
    #Moteur
    GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
    
    #Electrovanne
    GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(6, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)



print("Pin pompe")
pinPump = int(input())
setupGPIO()

if pinPump == 17:
    timePompe = 21
elif pinPump == 27:
    timePompe = 23
else:
    GPIO.output(13,GPIO.HIGH)
    timePompe = 18 #252 temps charge complète



GPIO.output(int(pinPump),GPIO.HIGH)
time.sleep(timePompe)
GPIO.output(int(pinPump),GPIO.LOW)
GPIO.output(13,GPIO.LOW)
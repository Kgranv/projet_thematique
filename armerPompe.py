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

def armedPump(pinPump,timePump):
    GPIO.output(int(pinPump),GPIO.HIGH)
    time.sleep(timePump)
    GPIO.output(int(pinPump),GPIO.LOW)
    GPIO.output(13,GPIO.LOW)

print("Armage des pompes")
setupGPIO()

GPIO.output(5,GPIO.HIGH)
armedPump(17,21)
armedPump(27,23)
GPIO.output(13,GPIO.HIGH)
armedPump(22,30)
GPIO.output(13,GPIO.LOW)
GPIO.output(5,GPIO.LOW)
GPIO.output(6,GPIO.HIGH)
armedPump(22,200)
GPIO.output(6,GPIO.LOW)
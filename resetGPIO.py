import RPi.GPIO as GPIO

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

print("Reset GPIO !")
setupGPIO()
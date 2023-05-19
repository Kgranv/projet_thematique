import asyncio
import time
import RPi.GPIO as GPIO

def setupPWM(pinMotor:list,pinVanne:list):
    """
    Setup GPIO PWM with a frequency of 0.1Hz
    """
    frequencyPWM = 10
    moteur = [GPIO.PWM(pinMotor[0],frequencyPWM),GPIO.PWM(pinMotor[1],frequencyPWM),GPIO.PWM(pinMotor[2],frequencyPWM)]
    return moteur

def setupGPIO():
    """
    Setup GPIO for control
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)

async def runPompe(index,dutyCycle):
    print("Demarage pompe ",index)
    motor[index].start(dutyCycle)
    await asyncio.sleep(60*2)
    motor[index].stop()
    print("Fin test pompe ",index)

async def main():
    dc = [50.0,54.2,58.3,62.5,66.7,70.8,75.0,79.2,83.3,87.5,91.7,95.8,100]
    tension = [6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5,12.0]
    test = []
    for x in range(0,len(dc)):
        print("Test avec une tension de ",tension[x]," V :")
        input('Presser entrer pour commencer ')
        for i in range(0,3):
            test.append(asyncio.create_task(runPompe(motor[i],dc[x])))
        await test[0]
        await test[1]
        await test[2]
        test = []
    print("Test terminée")

setupGPIO()
motor = setupPWM([17,27,22])
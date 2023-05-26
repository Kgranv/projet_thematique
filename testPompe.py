import asyncio
import time
import RPi.GPIO as GPIO

def setupPWM(pinMotor:list):
    """
    Setup GPIO PWM with a frequency of 0.1Hz
    """
    frequencyPWM = 100
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

def endProgram():
    """
    Clean all GPIO used for clean ending
    """
    GPIO.cleanup()

async def runPompe(index,dutyCycle):
    print("Demarage pompe ",index)
    motor[index].start(dutyCycle)
    await asyncio.sleep(60)
    motor[index].stop()
    print("Fin test pompe ",index)

async def main():
    dc = [100]
    tension = [12.0]
    test = []
    for x in range(0,len(dc)):
        print("Test avec une tension de ",tension[x]," V :")
        input('Presser entrer pour commencer ')
        for i in range(0,3):
            test.append(asyncio.create_task(runPompe(i,dc[x])))
        await test[0]
        await test[1]
        await test[2]
        test = []
    print("Test terminée")
    input('Presser entrer pour terminer ')
    endProgram()

setupGPIO()
motor = setupPWM([17,27,22])
asyncio.run(main())
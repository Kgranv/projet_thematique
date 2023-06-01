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
    #Moteur
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    
    #Electrovanne
    GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(6, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)

def endProgram():
    """
    Clean all GPIO used for clean ending
    """
    for i in range(0,3):
        motor[i].stop()
        GPIO.output[electrovanne[i],GPIO.LOW]

def checkInput(userInput,menu=0):
    try:
        userInput = int(userInput)
        match menu:
            case 0:
                #menu0
                if userInput>0 and userInput<5:
                    return False,userInput
                else:
                    raise
            case 1:
                #index
                if userInput>-1 and userInput<3:
                    return False,userInput
                else:
                    raise
            case 2:
                #dc
                if userInput>=0 and userInput<=100:
                    return False,userInput
                else:
                    raise
            case 3:
                #timeRun
                if userInput>0 and userInput<=120:
                    return False,userInput
                else:
                    raise
            case _:
                raise
    except:
        print("Je n'ai pas compris votre commande")
        return True

def getInput(menu=0):
    isWrongInput = True
    while isWrongInput:
        userInput = input()
        isWrongInput, userInput = checkInput(userInput,menu)
    return userInput
    
async def menu0():
    print("Que voulez vous tester ? :")
    print("1. Tout\n2. Moteur\n3. Electrovanne\n4. Fin du test")
    return getInput(0)
    

async def menu1():
    print("dutyCycle à utiliser ?")
    dc = getInput(2)
    print("Pendant combien de temps ?")
    timeRun = getInput(3)
    taskTestAll = asyncio.create_task(testAll(dc,timeRun))
    await taskTestAll

async def menu2():
    print("Quelle pompe voulez vous tester (0,1,2)? :")
    index = getInput(1)
    print("dutyCycle à utiliser ?")
    dc = getInput(2)
    print("Pendant combien de temps ?")
    timeRun = getInput(3)
    taskTestPompe = asyncio.create_task(runPompe(index,dc,timeRun))

async def menu3():
    print("Quelle electrovanne voulez vous tester (0,1,2)? :")
    index = getInput(1)
    print("Pendant combien de temps ?")
    timeRun = getInput(3)
    taskTestElectrovanne = asyncio.create_task(runPompe(index,timeRun))

async def runPompe(index,dutyCycle=100,timeRun=10):
    print("Demarage pompe ",index," pendant ",timeRun," seconde")
    motor[index].start(dutyCycle)
    await asyncio.sleep(timeRun)
    motor[index].stop()
    print("Fin test pompe ",index)

async def runElectrovanne(index,timeRun=10):
    print("Activation electrovanne ",index," pendant ",timeRun," seconde")
    GPIO.output(electrovanne[index], GPIO.HIGH)
    await asyncio.slepp(timeRun)
    GPIO.output(electrovanne[index], GPIO.LOW)
    print("Désactivation electrovanne ",index)

async def testAll(dutyCycle=100, timeRun=60):
    print("Test avec une tension de ",round(12*(dutyCycle/100),1)," V :")
    input('Presser entrer pour commencer ')
    for i in range(0,3):
        testPompe.append(asyncio.create_task(runPompe(i,dutyCycle,timeRun)))
        testElectroVanne.append(asyncio.create_task(runElectrovanne(i,timeRun)))
    await testPompe[0]
    await testPompe[1]
    await testPompe[2]
    await testElectroVanne[0]
    await testElectroVanne[1]
    await testElectroVanne[2]
    testPompe=[]
    testElectroVanne=[]
    print("Test terminée")
    input('Presser entrer pour terminer ')

async def main():
    while isRunning:
        nextMenu = asyncio.run(menu0())
        match nextMenu:
            case 1:
                asyncio.run(menu1())
            case 2:
                asyncio.run(menu2())
            case 3:
                asyncio.run(menu3())
            case 4:
                break
    endProgram()

setupGPIO()
motor = setupPWM([17,27,22])
electrovanne = [5,6,13]
testPompe = []
testElectroVanne = []
isRunning = True
asyncio.run(main())
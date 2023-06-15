import os
import time

outputFile = "./output.log"
controlFile = "./controle.csv"
isRunning = True
menuSelection = {"1":"Sample","2":"Observation","3":"Resume_cycle","4":"Log","5":"Stop","6":"Cancel"}
last_line = ""

def checkOs():
    """
    Check system OS if windows change path syntax
    """
    global outputFile
    global controlFile
    if os.name == "nt":
        outputFile = ".\\output.log"
        controlFile = ".\\controle.csv"

def prepareData(action,argument=""):
    global menuSelection
    return menuSelection[str(action)]+";"+str(argument)+"\n"

def writeControle(dataToWrite):
    global controlFile
    f = open(controlFile,"a")
    f.write(dataToWrite)
    f.close()

def readOutputFile():
    pass

def checkInput(userInput,menu=0):
    if menu == 0:
        try:
            userInput = int(userInput)
            if userInput >= 1 or userInput <=5:
                return False,userInput
            else:
                raise
        except:
            print("I don't understand your input")
            return True
    elif menu == 1:
        try:
            userInput = int(userInput)
            if userInput > 0:
                return False,userInput
            else:
                raise
        except:
            print("Please enter a number")
            return True

def getInput(menu=0):
    isWrongInput = True
    while isWrongInput:
        userInput = input()
        isWrongInput, userInput = checkInput(userInput,menu)
    return userInput

def printMenu():
    global menuSelection
    print("=========================")
    print("What do you want to do ? :")
    for index in menuSelection:
        print(index,". ",menuSelection[index])

def getLastLine():
    global outputFile
    with open(outputFile, "r") as file:
        lines = file.readlines()
        if lines:
            return lines[-1].strip()
        else:
            return ""
    
def menu0():
    global isRunning

    printMenu()
    userInput = getInput()
    if userInput >=1 and userInput <=5:
        if userInput == 1:
            print("Indicate the volume you are going to sample in mL :")
            argumentInput = getInput(userInput)
        elif userInput == 4:
            print("======Last line of the log ======")
            return
        else:
            argumentInput = "None"
        writeControle(prepareData(userInput,argumentInput))
    else:
        isRunning = False

checkOs()
while isRunning:
    menu0()
    if isRunning:
        time.sleep(0.5)
        print(getLastLine())
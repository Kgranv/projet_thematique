import pandas as pd
import os
import time

outputFile = "./output.log"
controlFile = "./controle.csv"
isRunning = True
menuSelection = {"1":"Prelevement","2":"Observation","3":"Stop","4":"Annuler"}
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
            if userInput >= 1 or userInput <=4:
                return False,userInput
            else:
                raise
        except:
            print("Je n'ai pas compris votre commande")
            return True
    elif menu == 1:
        try:
            userInput = int(userInput)
            if userInput > 0:
                return False,userInput
            else:
                raise
        except:
            print("Veuillez rentrer un nombre")
            return True

def getInput(menu=0):
    isWrongInput = True
    while isWrongInput:
        userInput = input()
        isWrongInput, userInput = checkInput(userInput,menu)
    return userInput

def printMenu():
    global menuSelection
    print("Que voulez vous faire ? :")
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
    if userInput >=1 and userInput <=3:
        if userInput == 1:
            print("Indiquer le volume que vous allez prélever en mL :")
            argumentInput = getInput(userInput)
        else:
            argumentInput = "None"
        writeControle(prepareData(userInput,argumentInput))
    else:
        isRunning = False

checkOs()
while isRunning:
    menu0()
    new_line = getLastLine()
    if new_line != last_line:
        print(new_line)
        last_line = new_line
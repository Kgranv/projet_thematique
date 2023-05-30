import pandas as pd
import os
import time

logPath = "./"
logFile = "log.csv"
logDataFrame = pd.DataFrame()
listeSelection = "1. print\n2. stop"
isWrongInput = True
userInput = 0

def checkOs():
    """
    Check system OS if windows change path syntax
    """
    if os.name == "nt":
        logPath = ".\\"
        
def openFile():
    fullPath = logPath+logFile
    return pd.read_csv(fullPath, sep=";", header=None, names=["Status", "Action", "Argument"])

def addRow(action):
    global logDataFrame
    rowToAdd = pd.DataFrame({"Status": ["pending"], "Action": [action[0]], "Argument": [action[1]]})
    logDataFrame = pd.concat([logDataFrame, rowToAdd], ignore_index=True)

def updateLogFile():
    logDataFrame.to_csv(logPath+logFile,header=None,sep=";",index=False)

def checkInput():
    global userInput
    global isWrongInput
    try:
        userInput = int(userInput)
        isWrongInput = False
        if userInput == 1:
            actionToReturn = "print"
        elif userInput == 2:
            actionToReturn = "stop"
        else:
            isWrongInput = True
            raise
        return actionToReturn
    except:
        print("Je n'ai pas compris votre commande.")
        isWrongInput = True


checkOs()
logDataFrame = openFile()

while isWrongInput:
    userInput = input("Que voulez vous faire ? :\n"+listeSelection+"\n")
    actionToDo = checkInput()

argument = input("Arg\n")
if actionToDo != "stop":
    actionToDo = "print"

addRow([actionToDo,argument])
updateLogFile()
import pandas as pd
import os
import time

logPath = "./"
logFile = "log.csv"
logDataFrame = pd.DataFrame()
listeSelection = ["prélevement","observation","stop","annuler"]
isWrongInput = True
userInput = 0
isRunning = True

file_path = "./output.log"
new_line = ""
last_line = ""

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

def getInput():
    print("Que voulez vous faire ? :")
    for x in range(0,len(listeSelection)):
        print(str(x+1)+". "+listeSelection[x])
    return input()

def checkInput():
    global userInput
    global isWrongInput
    try:
        userInput = int(userInput)
        isWrongInput = False
        if userInput > 0 and userInput < len(listeSelection)+1:
            actionToReturn = listeSelection[userInput-1]
        else:
            isWrongInput = True
            raise
        return actionToReturn
    except:
        print("Je n'ai pas compris votre commande.")
        isWrongInput = True

checkOs()
logDataFrame = openFile()

while isRunning:
    while isWrongInput:
        userInput = getInput() 
        actionToDo = checkInput()

    if actionToDo == "annuler":
        isRunning = False
    else:
        argument = input("Arg\n")
        if actionToDo != "stop":
            actionToDo = "print"
        addRow([actionToDo,argument])
        isWrongInput = True
    updateLogFile()

    time.sleep(1)
    with open(file_path, "r") as file:
            lines = file.readlines()
            if lines:
                new_line = lines[-1].strip()
    if new_line != last_line:
        print("Dernière ligne du fichier : ", new_line)
        last_line = new_line
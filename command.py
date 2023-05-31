import pandas as pd
import os
import time

commandPath = "./"
commandFile = "command.csv"
commandDataFrame = pd.DataFrame()
listeSelection = ["prélevement","observation","stop","print","annuler"]
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
        commandPath = ".\\"
        file_path = ".\\output.log"
        
def openFile():
    fullPath = commandPath+commandFile
    return pd.read_csv(fullPath, sep=";", header=None, names=["Status", "Action", "Argument"])

def addRow(action):
    global commandDataFrame
    rowToAdd = pd.DataFrame({"Status": ["pending"], "Action": [action[0]], "Argument": [action[1]]})
    commandDataFrame = pd.concat([commandDataFrame, rowToAdd], ignore_index=True)

def updatecommandFile():
    commandDataFrame.to_csv(commandPath+commandFile,header=None,sep=";",index=False)

def getActionInput():
    print("Que voulez vous faire ? :")
    for x in range(0,len(listeSelection)):
        print(str(x+1)+". "+listeSelection[x])
    return input()

def getArgInput(argumentType=0):
    if argumentType == 0:
        return input("Indiquer le volume prélevé en mL\n")
    else:
        return input("Entrer argument\n")

def checkActionInput():
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
    
def checkArgInput(argumentType=0, argInput=0):
    if argumentType == 0:
        try:
            argInput = int(argInput)
            if argInput > 0:
                return False, argInput
            else:
                raise
        except:
            print("Je n'ai pas compris votre commande.")
            return True, 0
    else:
        return False, argInput

def getLastLine():
    with open(file_path, "r") as file:
        lines = file.readlines()
        if lines:
            return lines[-1].strip()
        else:
            return ""

checkOs()
commandDataFrame = openFile()

while isRunning:
    while isWrongInput:
        userInput = getActionInput() 
        actionToDo = checkActionInput()

    if actionToDo == listeSelection[len(listeSelection)-1]:
        isRunning = False
        break
    else:
        if actionToDo == listeSelection[0]:
            isWrongInput = True
            while isWrongInput:
                argument= getArgInput()
                isWrongInput,argument = checkArgInput(argInput=argument)
        elif actionToDo == listeSelection[3]:
            argument = input("Argument\n")
        else:
            argument = "None"
        addRow([actionToDo,argument])
    
    updatecommandFile()
    isWrongInput = True

    time.sleep(1)

    new_line = getLastLine()
    if new_line != last_line:
        print("Dernière ligne du fichier : ", new_line)
        last_line = new_line
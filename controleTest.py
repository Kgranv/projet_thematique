import pandas as pd
import os
import time

outputFile = "./output.log"
controlFile = "./controle.csv"
menuSelection = {"1":"prelevement","2":"Observation","3":"stop","4":"annuler"}
def checkOs():
    """
    Check system OS if windows change path syntax
    """
    if os.name == "nt":
        commandPath = ".\\"
        file_path = ".\\output.log"

def writeControle(dataToWrite):
    pass

def readOutputFile():
    pass

def printMenu():
    print("Que voulez vous faire ? :")
    for index in menuSelection:
        print(index,". ",menuSelection[index])

checkOs()
printMenu()
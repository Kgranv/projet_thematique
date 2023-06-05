import pandas as pd
import os
import sys
import threading
from datetime import datetime

outputFileName = "output.log"
outputFilePath = "./"+outputFileName
controleFile = "./controle.csv"
updateConcentration = False
timeBetweenChange = 1
isSuspended = False
isStop = False
volumeTotal = 20
scheduleConcentration = None

class Tee(object):
    def __init__(self, file_name=outputFileName):
        self.file = open(file_name, "a")

    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self.stdout
        self.file.close()

    def write(self, message):
        self.file.write(message)
        self.file.flush()
        self.stdout.write(message)

def checkOs():
    """
    Check system OS if windows change path syntax
    """
    global outputFileName
    global outputFilePath
    global controleFile
    if os.name == "nt":
        outputFilePath = ".\\"+outputFileName
        controleFile = ".\\controle.csv"

def removeLine():
    """
    Remove the first line of controlFile
    """
    global controleFile
    with open(controleFile, 'r+') as file:
        # read an store all lines into list
        lines = file.readlines()
        # move file pointer to the beginning of a file
        file.seek(0)
        # truncate the file
        file.truncate()
        file.writelines(lines[1:])

def getFirstLine():
    """
    Return the first line of controlFile
    """
    global controleFile
    with open(controleFile,"r") as file:
        line = file.readline()
        return line[:len(line)-1]

def prepareAction(line):
    commaIndex = line.find(";")
    actionToDo = line[:commaIndex]
    argument = line[commaIndex+1:]
    return actionToDo, argument

def doAction(actionToDo, argument):
    global isSuspended
    global isStop
    global volumeTotal

    if actionToDo == "Prelevement":
        volumeTotal = volumeTotal-int(argument)
    elif actionToDo == "Observation":
        isSuspended = True
    elif actionToDo == "Reprendre_cycle":
        isSuspended = False
    elif  actionToDo == "Stop":
        isStop = True


def readConcentration():
    print(volumeTotal)

def changeConcentration():
    global timeBetweenChange
    global isSuspended
    global isStop
    global scheduleConcentration

    if isSuspended:
        if scheduleConcentration is not None and scheduleConcentration.is_alive():
            scheduleConcentration.cancel()
    else:
        readConcentration()

    if isStop:
        pass
    else:
        scheduleConcentration = threading.Timer(timeBetweenChange * 10, changeConcentration).start()

checkOs()
changeConcentration()
while not isStop:
    if getFirstLine() != "":
        actionToDo, argument = prepareAction(getFirstLine())
        with Tee():
            print("action : ",actionToDo," argument : ", argument )
        doAction(actionToDo, argument)
        removeLine()

if scheduleConcentration is not None and scheduleConcentration.is_alive():
    scheduleConcentration.cancel()
print("completely stop")
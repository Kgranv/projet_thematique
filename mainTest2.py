import pandas as pd
import os
import sys
import threading
import time

outputFileName = "output.log"
outputFilePath = "./"+outputFileName
controleFile = "./controle.csv"
concentrationFile = ""
concentrationFilePath = "./Data/"

class Pompe():
    debit = 0
    id = ""
    
    def __init__(self,newDebit,newId):
        self.debit = newDebit
        self.id = newId

    def injection(self,quantity):
        print(self.timeToRun(quantity))

    def timeToRun(self,quantity):
        return int((quantity/self.debit)*60)

class Electrovanne():
    id = ""

    def __init__(self,id):
        self.id

    def open(self):
        print("Ouverture")

    def close(self):
        print("Fermeture")

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


updateConcentration = False
isSuspended = False
isStop = False

timeBetweenChange = 1
volumeTotal = 20
startTime = 0

scheduleConcentration = None

debitPompe = [1.0549,1.3314,1.3197]
listePompe = [Pompe(debitPompe[0],"flow"),Pompe(debitPompe[1],"conc1"),Pompe(debitPompe[2],"conc2")]
listeVanne = [Electrovanne("purge"),Electrovanne("cells1"),Electrovanne("cells2")]


def checkOs():
    """
    Check system OS if windows change path syntax
    """
    global outputFileName
    global outputFilePath
    global controleFile
    global concentrationFilePath
    if os.name == "nt":
        outputFilePath = ".\\"+outputFileName
        controleFile = ".\\controle.csv"
        concentrationFilePath = ".\\Data\\"

def getArg():
    global concentrationFilePath
    global concentrationFile
    print(sys.argv)
    if len(sys.argv) == 2:
        try:
            concentrationFile = pd.read_feather(concentrationFilePath+sys.argv[1])
            return True
        except:
            with Tee():
                print("Unable to open concentration file")
            return False
    elif len(sys.argv) == 3:
        try:
            concentrationFile = pd.read_feather(concentrationFilePath+sys.argv[1])
            print("=========Debug mode=========")
            print(type(concentrationFile["Time"].iloc[86400]))
            return False
        except:
            with Tee():
                print("Unable to open concentration file")
            return False
    elif len(sys.argv) == 1:
        with Tee():
            print("Please indicate which data you would use.")
    else:
        with Tee():
            print("Too many argument. I take only 1 argument.")
        return False

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
        isSuspended = True
        volumeTotal = volumeTotal-int(argument)
    elif actionToDo == "Observation":
        isSuspended = True
    elif actionToDo == "Reprendre_cycle":
        isSuspended = False
    elif  actionToDo == "Stop":
        isStop = True

def getConc():
    global startTime
    timeInSecond = int(time.monotonic()-startTime)
    print("Temps écoulé en seconde : ",timeInSecond)
    conc1 = concentrationFile["Conc1"].iloc[timeInSecond]
    conc2 = concentrationFile["Conc2"].iloc[timeInSecond]
    nutConc = 100.0-conc1-conc2
    return nutConc,conc1,conc2

def startPurge(purgeTime):
    for vanne in listeVanne:
        if vanne.id=="purge":
            vanne.open()
        else:
            vanne.close()
    time.sleep(purgeTime)
    for vanne in listeVanne:
        if vanne.id=="purge":
            vanne.close()
        else:
            vanne.open()

def changeConcentration():
    global timeBetweenChange
    global isSuspended
    global isStop
    global scheduleConcentration
    global listePompe

    if isSuspended:
        if scheduleConcentration is not None and scheduleConcentration.is_alive():
            scheduleConcentration.cancel()
    else:
        nutConc,conc1,conc2 = getConc()
        #Appel code calcul injection

        purge = False
        injectConc1 = 2
        injectConc2 = 1
        timePurge = 0
        if purge:
            startPurge(timePurge)
        
        for vanne in listeVanne:
            if vanne.id == "cells1" or vanne.id=="cells2":
                vanne.close()

        for pump in listePompe:
            if pump.id == "conc1":
                pump.injection(injectConc1)
            if pump.id == "conc2":
                pump.injection(injectConc2)

        for vanne in listeVanne:
            if vanne.id == "cells1" or vanne.id=="cells2":
                vanne.open()

    if isStop:
        pass
    else:
        scheduleConcentration = threading.Timer(timeBetweenChange * 10, changeConcentration)
        scheduleConcentration.start()

checkOs()
if getArg():
    startTime = time.monotonic()
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
        print("Wololo")
    with Tee():
        print("completely stop")
else:
    pass
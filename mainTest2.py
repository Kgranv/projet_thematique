import pandas as pd
import os
import sys
from datetime import datetime

outputFileName = "output.log"
outputFilePath = "./"+outputFileName
controleFile = "./controle.csv"

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
    global controleFile
    with open(controleFile,"r") as file:
        line = file.readline()
        return line[:len(line)-1]

def prepareAction(line):
    commaIndex = line.find(";")
    actionToDo = line[:commaIndex]
    argument = line[commaIndex+1:]
    return actionToDo, argument
checkOs()
while True:
    if getFirstLine() != "":
        with Tee():
            print(prepareAction(getFirstLine()))
        removeLine()
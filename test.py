import pandas as pd
import os
import sys

class Tee(object):
    def __init__(self, file_name="output.log"):
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



logPath = "./"
logFile = "log.csv"
logDataFrame = pd.DataFrame()
isRunning = True
listAction = ["prélevement","observation","stop","print"]

def checkOs():
    """
    Check system OS if windows change path syntax
    """
    if os.name == "nt":
        logPath = ".\\"
        
def openFile():
    fullPath = logPath+logFile
    return pd.read_csv(fullPath, sep=";", header=None, names=["Status", "Action", "Argument"])

def addMissingRows(df1, df2):
    if len(df1) < len(df2):
        missing_rows = df2.iloc[len(df1):]
        df1 = pd.concat([df1, missing_rows], ignore_index=True)
    return df1

def doAction():
    global logDataFrame
    global isRunning
    pending_rows = logDataFrame.loc[logDataFrame["Status"] == "pending"]
    
    for index, row in pending_rows.iterrows():
        logDataFrame.at[index, "Status"] = "done"
        if row["Action"] == listAction[0]:
            #do action for prélèvement
            with Tee():
                print("Vous pouvez maintenant faire un prélèvement")
        elif row["Action"] == listAction[1]:
            #do action for observation
            with Tee():
                print("Vous pouvez maintenant faire une observation")
        elif row["Action"] == listAction[2]:
            #do action for stop
            isRunning = False
            with Tee():
                print("normaly stop")
            break
        elif row["Action"] == listAction[len(listAction)-1]:
            with Tee():
                print(row["Argument"])
    logDataFrame = addMissingRows(logDataFrame,openFile())
    updateLogFile()

def updateLogFile():
    logDataFrame.to_csv(logPath+logFile,header=None,sep=";",index=False)    


sys.stdout = sys.__stdout__
checkOs()
while isRunning:
    logDataFrame = openFile()
    doAction()
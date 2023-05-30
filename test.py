import pandas as pd
import os
import sys

logPath = "./"
logFile = "log.csv"
logDataFrame = pd.DataFrame()
isRunning = True

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
        if row["Action"] == "print":
            print(row["Argument"])
        elif row["Action"] == "stop":
            isRunning = False
            print("normaly stop")
            break
    logDataFrame = addMissingRows(logDataFrame,openFile())
    updateLogFile()

def updateLogFile():
    logDataFrame.to_csv(logPath+logFile,header=None,sep=";",index=False)    


sys.stdout = sys.__stdout__
checkOs()
while isRunning:
    logDataFrame = openFile()
    doAction()
print(logDataFrame)
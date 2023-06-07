import os
import numpy as np
import pandas as pd
from datetime import datetime

userDataFolder = "userData"
userDataPath = "./"+userDataFolder+"/"
dataFolder = "data"
dataPath = "./"+dataFolder+"/"
timeMax = 2419200
userData = 0

def checkOs():
    """
    Check system OS if windows change path syntax
    """
    global userDataPath
    global dataPath
    global dataFolder
    if os.name == "nt":
        userDataPath = ".\\"+userDataFolder+"\\"
        dataPath = ".\\"+dataFolder+"\\"

def checkFolder(folder):
    """
    Check if folder exist if not create it.
    return true if exist, if not return false
    """
    if not os.path.isdir(folder):
        os.makedirs(folder)
        print("created folder : ",folder)
        return False
    else:
        return True

def openUserData():
    """
    Ask for wich user data to use.
    Check if it's usable. return an array if usable, return 0 if it's not usable
    """
    global userDataPath
    global userDataName
    userDataName = input("data to convert : ")
    try:
        completePath = userDataPath+userDataName
        importedCSV = pd.read_csv(completePath,sep=",")
        userDataTime = importedCSV["time"].to_numpy()
        userDataConc1 = importedCSV["conc1"].to_numpy()
        userDataConc2 = importedCSV["conc2"].to_numpy()
        return np.vstack([userDataTime,userDataConc1,userDataConc2]).astype(float)

    except:
        print("Error ! unable to open : ",userDataName)
        return 0

def createUsableTable(userData):
    """
    Create a table with intermediate point.
    """
    global timeMax

    # interpolate values
    timeTable = np.arange(userData[0][0], userData[0][-1]+1)
    conc1Table = np.interp(timeTable, userData[0], userData[1])
    conc2Table = np.interp(timeTable, userData[0], userData[2])
    timeTable = timeTable.astype(np.int64)
    conc1Table = np.around(conc1Table,3)
    conc2Table = np.around(conc2Table,3)
    return np.vstack([timeTable, conc1Table, conc2Table]).T

def createFtr(dataTable):
    """
    Create a ftr with all point usable for control the bio-chip
    """
    global dataFolder
    global dataPath
    checkFolder(dataFolder)
    #generate the name of the file based on time
    fileName = datetime.now()
    fileName = fileName.strftime("%Y-%m-%d_%H%M%S")
    fileExtension = ".ftr"
    file = dataPath+fileName+fileExtension
    try:
        df = pd.DataFrame(dataTable,columns=["Time","Conc1","Conc2"])
        df["Time"]=df["Time"].astype("int")
        df.to_feather(file)
        print("Conversion completed !")
    except:
        print("Unable to convert the data into a csv file.")


checkOs()
if checkFolder(userDataFolder):
    userData = openUserData()
    if(type(userData)==np.ndarray):
        usableTable = createUsableTable(userData)
        createFtr(usableTable)
    else:
        print("Unable to prepare your data")
else:
    print(userDataFolder, " folder was created. Place your csv file to convert inside and run again the program.")


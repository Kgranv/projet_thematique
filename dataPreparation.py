import os
import numpy as np
import pandas as pd
from datetime import datetime

userDataFolder = "userData"
userDataPath = ".\\"+userDataFolder+"\\"
dataFolder = "data"
dataPath = ".\\"+dataFolder+"\\"
timeMax = 2419200
userData = 0

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
    #calculate slope
    slopeArrayConc1 = np.zeros(len(userData[0])-1)
    slopeArrayConc2 = np.zeros(len(userData[0])-1)
    for x in range(len(slopeArrayConc1)):
        slopeArrayConc1[x] = (userData[1][x+1]-userData[1][x])/(userData[0][x+1]-userData[0][x])
        slopeArrayConc2[x] = (userData[2][x+1]-userData[2][x])/(userData[0][x+1]-userData[0][x])
    
    #init first line
    timeTable = np.array([userData[0][0]])
    conc1Table = np.array([userData[1][0]])
    conc2Table = np.array([userData[2][0]])
    
    #fill the point between userpoint
    for x in range(1,len(userData[0])):
        timeTable = np.append(timeTable,np.arange(userData[0][x-1],userData[0][x],1))
        conc1Table = np.append(conc1Table,np.arange(userData[1][x-1],userData[1][x],slopeArrayConc1[x-1]))
        conc2Table = np.append(conc2Table,np.arange(userData[2][x-1],userData[2][x],slopeArrayConc2[x-1]))
    
    #fill the end of the table
    timeTable = np.append(np.array(timeTable[1:len(timeTable)]),np.arange(userData[0][len(userData[0])-1],timeMax+1,1,float))
    fillerTable = np.zeros(timeMax-len(conc1Table)+2)
    fillerTable.fill(userData[1][len(userData[0])-1])
    conc1Table = np.append(np.array(conc1Table[1:len(conc1Table)]),fillerTable)
    fillerTable.fill(userData[2][len(userData[0])-1])
    conc2Table = np.append(np.array(conc2Table[1:len(conc2Table)]),fillerTable)
    
    return np.vstack([timeTable,conc1Table,conc2Table]).T

def createFtr(dataTable):
    """
    Create a ftr with all point usable for control the bio-chip
    """
    checkFolder(dataFolder)
    #generate the name of the file based on time
    fileName = datetime.now()
    fileName = fileName.strftime("%Y-%m-%d_%H%M%S")
    fileExtension = ".ftr"
    file = dataPath+fileName+fileExtension

    try:
        df = pd.DataFrame(dataTable,columns=["Time","Conc1","Conc2"])
        df.to_feather(file)
        print("Conversion completed !")
    except:
        print("Unable to convert the data into a csv file.")

if checkFolder(userDataFolder):
    userData = openUserData()
    if(type(userData)==np.ndarray):
        usableTable = createUsableTable(userData)
        createFtr(usableTable)
    else:
        print("Unable to prepare your data")
else:
    print("userData folder was created. Place your csv file to convert inside and run again the program.")


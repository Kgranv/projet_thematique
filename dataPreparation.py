import numpy as np
import pandas as pd

userDataPath = ".\\userData\\"
timeMax = 2419200
userData = 0

def openUserData():
    userDataName = input("data to exploit : ")
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

def genTable():
    timeTable = np.arange(start=0,stop=timeMax+1,step=1)
    slopeConc1Table = np.zeros(timeMax+1,dtype=float)
    slopeConc2Table = np.zeros(timeMax+1,dtype=float)
    conc1Table = np.zeros(timeMax+1,dtype=float)
    conc2Table = np.zeros(timeMax+1,dtype=float)
    return np.vstack([timeTable,slopeConc1Table,slopeConc2Table,conc1Table,conc2Table])

def fillTable(userData,emptyTable):
    for x in range(len(userData[0])):
        if x != 0:
            i=int(userData[0][x-1]+1)
            slopeConc1 = (userData[1][x]-userData[1][x-1])/(userData[0][x]-userData[0][x-1])
            slopeConc2 = (userData[2][x]-userData[2][x-1])/(userData[0][x]-userData[0][x-1])
            while emptyTable[0][i] < userData[0][x]:
                emptyTable[1][i]=slopeConc1
                emptyTable[2][i]=slopeConc2
                i+=1
        emptyTable[1][int(userData[0][x])] = 0
        emptyTable[2][int(userData[0][x])] = 0
        emptyTable[3][int(userData[0][x])] = userData[1][x]
        emptyTable[4][int(userData[0][x])] = userData[2][x]
    for x in range(len(emptyTable[0])):
        if emptyTable[1][x] != 0:
            emptyTable[3][x] = emptyTable[1][x]+emptyTable[3][x-1]
        if emptyTable[2][x] != 0:
            emptyTable[4][x] = emptyTable[2][x]+emptyTable[4][x-1]
    return emptyTable

userData = openUserData()

if(type(userData)==np.ndarray):
    emptyTable = genTable()
    test = fillTable(userData,emptyTable)
    print(test)

else:
    print("Unable to prepare your data")


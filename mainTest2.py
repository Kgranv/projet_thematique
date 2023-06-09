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

    def on(self):
        print("Ouverture")

    def off(self):
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
listePompe = [Pompe(debitPompe[0],"conc1"),Pompe(debitPompe[1],"conc2"),Pompe(debitPompe[2],"flow")]
listeVanne = [Electrovanne("purge"),Electrovanne("cells"),Electrovanne("nut")]

lastNutConc = 0
lastConc1 = 0
lastConc2 = 0

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

    if len(sys.argv) == 1:
        with Tee():
            print("Please indicate which data you would use.")
    
    elif len(sys.argv) == 2:
        try:
            concentrationFile = pd.read_feather(concentrationFilePath+sys.argv[1])
            return True
        except:
            with Tee():
                print("Unable to open concentration file")
            return False
    
    elif len(sys.argv) == 3:
        if sys.argv[2] == "Debug":
            try:
                concentrationFile = pd.read_feather(concentrationFilePath+sys.argv[1])
                with Tee():
                    print("=========Debug mode=========")
                    print(type(concentrationFile["Time"].iloc[86400]))
                return False
            except:
                with Tee():
                    print("Unable to open concentration file")
                return False
        elif sys.argv[2] == "Demo":
            try:
                concentrationFile = pd.read_feather(concentrationFilePath+sys.argv[1])
                return True
            except:
                with Tee():
                    print("Unable to open concentration file")
                return False
        else:
            with Tee():
                print("I don't understand")
            return False
    
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
        for vanne in listeVanne:
            if vanne.id=="cells":
                vanne.off()
    elif actionToDo == "Observation":
        isSuspended = True
        for vanne in listeVanne:
            if vanne.id=="cells":
                vanne.off()
    elif actionToDo == "Reprendre_cycle":
        isSuspended = False
        for vanne in listeVanne:
            if vanne.id=="cells":
                vanne.on()
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
        vanne.on()

    time.sleep(purgeTime)

    for vanne in listeVanne:
        vanne.off()

def purge(concentration_c1_mtn,concentration_c2_mtn, concentration_c1_apres, concentration_c2_apres, volume_circuit ):
    concentration_nut_mtn=1-concentration_c1_mtn-concentration_c2_mtn
    concentration_nut_apres=1-concentration_c1_apres-concentration_c2_apres
    volume_min = 3 # le volume mini a avoir sur le circuit
    purge=False
    volume_purge=0.0
    if (concentration_nut_apres <=concentration_nut_mtn):
       purge=False
       volume_purge=0.0 
    elif (concentration_nut_apres > concentration_nut_mtn):
        volume_mtn_nut = concentration_nut_mtn*volume_circuit
        volume_mtn_c1 = concentration_c1_mtn*volume_circuit
        volume_mtn_c2 = concentration_c2_mtn*volume_circuit
        
        volume_apres_nut = concentration_c1_apres*volume_min
        volume_apres_c1 = concentration_c2_apres*volume_min
        volume_apres_c2 = concentration_nut_apres*volume_min
        
        volume_pour_purge=0
        
        volume_reste_purge_nut = volume_mtn_nut-(volume_pour_purge*concentration_nut_mtn)
        volume_reste_purge_c1 = volume_mtn_c1-(volume_pour_purge*concentration_c1_mtn)
        volume_reste_purge_c2 = volume_mtn_c2-(volume_pour_purge*concentration_c2_mtn)
        volume_tot_reste_purge = volume_circuit-volume_pour_purge
        
        
        while (volume_reste_purge_nut>volume_apres_nut or volume_reste_purge_c1>volume_apres_c1 or volume_reste_purge_c2>volume_apres_c2):
            
            volume_reste_purge_nut = volume_mtn_nut-(volume_pour_purge*concentration_nut_mtn)
            volume_reste_purge_c1 = volume_mtn_c1-(volume_pour_purge*concentration_c1_mtn)
            volume_reste_purge_c2 = volume_mtn_c2-(volume_pour_purge*concentration_c2_mtn)
            volume_tot_reste_purge = volume_circuit-volume_pour_purge
            volume_pour_purge=volume_pour_purge+1
            
        
        if (volume_tot_reste_purge<volume_min):
            volume_pour_purge=volume_circuit-volume_min
            
        
        purge=True
        volume_purge=round(volume_pour_purge,2)
            
    return purge, volume_purge

def ajout(concentration_c1_mtn,concentration_c2_mtn, concentration_c1_apres, concentration_c2_apres, volume_circuit, volume_purge):
    concentration_nut_mtn=1-concentration_c1_mtn-concentration_c2_mtn
    concentration_nut_apres=1-concentration_c1_apres-concentration_c2_apres
    volume=3
    volume_max=50
    add=[]
    if (volume_purge==0):
        add_nut=0
        add_c1 = ((-concentration_nut_apres*concentration_c1_mtn*volume_circuit)+(concentration_nut_mtn*concentration_c1_apres*volume_circuit)+(concentration_c1_apres*add_nut))/concentration_nut_apres
        add_c2 = -(((concentration_c1_apres-1)*((concentration_nut_mtn*volume_circuit)+add_nut))/concentration_nut_apres)+(concentration_c1_mtn-1)*(volume_circuit-add_nut)
    elif (volume_purge!=0):
        volume_mtn_nut = concentration_nut_mtn*volume_circuit
        volume_mtn_c1 = concentration_c1_mtn*volume_circuit
        volume_mtn_c2 = concentration_c2_mtn*volume_circuit
        
        volume_apres_nut = concentration_nut_apres*volume
        volume_apres_c1 = concentration_c1_apres*volume
        volume_apres_c2 = concentration_c2_apres*volume
        
        volume_pour_purge=volume_purge
        
        volume_reste_purge_nut = volume_mtn_nut-(volume_pour_purge*concentration_nut_mtn)
        volume_reste_purge_c1 = volume_mtn_c1-(volume_pour_purge*concentration_c1_mtn)
        volume_reste_purge_c2 = volume_mtn_c2-(volume_pour_purge*concentration_c2_mtn)
        
        
        add_nut = volume_apres_nut-volume_reste_purge_nut
        add_c1 = volume_apres_c1-volume_reste_purge_c1
        add_c2 = volume_apres_c2-volume_reste_purge_c2
        
        #si une concentration arrive a 0 : purge le max et rajoute le max?
        if (volume_apres_nut==0 or volume_apres_c1==0 or volume_apres_c2==0):
            volume = volume_max
            volume_apres_nut = concentration_nut_apres*volume
            volume_apres_c1 = concentration_c1_apres*volume
            volume_apres_c2 = concentration_c2_apres*volume
            
            add_nut = volume_apres_nut-volume_reste_purge_nut
            add_c1 = volume_apres_c1-volume_reste_purge_c1
            add_c2 = volume_apres_c2-volume_reste_purge_c2
            if (volume_apres_nut==0):
                add_nut=0
            if (volume_apres_c1==0):
                add_c1=0
            if (volume_apres_c2==0):
                add_c2=0
            
        else : 
            while (add_nut<0 or add_c1<0 or add_c2<0):
                volume+=1
                volume_apres_nut = concentration_nut_apres*volume
                volume_apres_c1 = concentration_c1_apres*volume
                volume_apres_c2 = concentration_c2_apres*volume
                
                add_nut = volume_apres_nut-volume_reste_purge_nut
                add_c1 = volume_apres_c1-volume_reste_purge_c1
                add_c2 = volume_apres_c2-volume_reste_purge_c2
    
    add=[round(add_nut,2),round(add_c1,2),round(add_c2,2)]
    
    return add # nutriment, c1, c2

def changeConcentration():
    global timeBetweenChange
    global isSuspended
    global isStop
    global scheduleConcentration
    global listePompe
    global lastNutConc
    global lastConc1
    global lastConc2
    global volumeTotal

    if isSuspended:
        if scheduleConcentration is not None and scheduleConcentration.is_alive():
            scheduleConcentration.cancel()
    else:
        nutConc,conc1,conc2 = getConc()

        isPurge, volumePurge = purge(lastConc1,lastConc2,conc1,conc2,volumeTotal)
        volInjection = ajout(lastConc1,lastConc2,conc1,conc2,volumeTotal,volumePurge)

        lastNutConc =nutConc
        lastConc1 =conc1
        lastConc2 =conc2

        for pump in listePompe:
            if pump.id == "flow":
                timePurge = volumePurge/pump.debit
                timeNut = volInjection[0]/pump.debit

        if isPurge:
            startPurge(timePurge)
        
        for vanne in listeVanne:
            if vanne.id == "purge" or vanne.id=="cells":
                vanne.off()
            else:
                vanne.on()

        time.sleep(timeNut)

        for vanne in listeVanne:
            vanne.off()

        for pump in listePompe:
            if pump.id == "conc1":
                pump.injection(volInjection[1])
            if pump.id == "conc2":
                pump.injection(volInjection[2])

        time.sleep(30)

        for vanne in listeVanne:
            if vanne.id == "cells":
                vanne.on()
            else:
                vanne.off()

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
    with Tee():
        print("completely stop")
else:
    pass
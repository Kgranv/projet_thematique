import pandas as pd
import os
import sys
import threading
import time
import RPi.GPIO as GPIO

outputFileName = "output.log"
outputFilePath = "./"+outputFileName
controleFile = "./controle.csv"
concentrationFile = ""
concentrationFilePath = "./data/"


class Pompe():
    debit = 0
    id = ""
    pinNumber = 0
    
    def __init__(self,newDebit,newId, newPin):
        self.debit = newDebit
        self.id = newId
        self.pinNumber = newPin

    def injection(self,quantity):

        #TURN ON PUMP
        GPIO.output(self.pinNumber,GPIO.HIGH)
        time.sleep(self.timeToRun(quantity))
        GPIO.output(self.pinNumber,GPIO.LOW)
        #TURN OFF PUMP

    def timeToRun(self,quantity):
        return int((quantity/self.debit)*60)
    
    def on(self):
        GPIO.output(self.pinNumber,GPIO.HIGH)
    def off(self):
        GPIO.output(self.pinNumber,GPIO.LOW)

class Electrovanne():
    id = ""
    pinNumber = 0

    def __init__(self,id,newPin):
        self.id = id
        self.pinNumber = newPin

    def on(self):
        GPIO.output(self.pinNumber,GPIO.HIGH)

    def off(self):
        GPIO.output(self.pinNumber,GPIO.LOW)

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

timeBetweenChange = 30
volumeTotal = 10.0
startTime = 0

scheduleConcentration = None

pinPompe = [17,27,22]
pinVanne = [5,6,13]
debitPompe = [1.0549,1.3314,1.3197]
listePompe = [Pompe(debitPompe[0],"conc1",pinPompe[0]),Pompe(debitPompe[1],"conc2",pinPompe[1]),Pompe(debitPompe[2],"flow",pinPompe[2])]
listeVanne = [Electrovanne("purge",pinVanne[0]),Electrovanne("cells",pinVanne[1]),Electrovanne("nut",pinVanne[2])]

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
    """
    Get argument when you start the script
    """
    global concentrationFilePath
    global concentrationFile
    global timeBetweenChange

    if len(sys.argv) == 1:
        with Tee():
            print("Please indicate which data you would use.")
    
    elif len(sys.argv) == 2:
        try:
            concentrationFile = pd.read_feather(concentrationFilePath+sys.argv[1])
            with Tee():
                print(getTime()+"|"+"Start sequence with file "+sys.argv[1])
            return True
        except:
            with Tee():
                print("Unable to open concentration file")
            return False
    
    elif len(sys.argv) == 3:
        #For debug only
        if sys.argv[2] == "debug":
            try:
                with Tee():
                    print("=========Debug mode=========")
                    print(getTime())
                return False
            except:
                with Tee():
                    print("Unable to open concentration file")
                return False
        elif sys.argv[2] == "demo":
            #For demo only
            try:
                concentrationFile = pd.read_feather(concentrationFilePath+sys.argv[1])
                timeBetweenChange = 5
                with Tee():
                    print(getTime()+"|""Start sequence with file "+sys.argv[1]+" for demo")
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
            print("Too many argument. I take only 1 argument. 2 For debug only.")
        return False
    
def getTime():
    actualDate = time.localtime()
    if actualDate.tm_mday < 10:
        day = "0"+str(actualDate.tm_mday)
    else:
        day = str(actualDate.tm_mday)

    if actualDate.tm_mon < 10:
        month = "0"+str(actualDate.tm_mon)
    else:
        month = str(actualDate.tm_mon)

    if actualDate.tm_hour < 10:
        hour = "0"+str(actualDate.tm_hour)
    else:
        hour = str(actualDate.tm_hour)

    if actualDate.tm_min < 10:
        minute = "0"+str(actualDate.tm_min)
    else:
        minute = str(actualDate.tm_min)

    dateToReturn = day+"."+month+"."+str(actualDate.tm_year)+" : "+hour+"h"+minute+"min"
    return dateToReturn

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
    """
    Prepare action to do
    """
    commaIndex = line.find(";")
    actionToDo = line[:commaIndex]
    argument = line[commaIndex+1:]
    return actionToDo, argument

def doAction(actionToDo, argument):
    """
    Do action. List of action : Prelevement, Observation, Reprendre cycle, Stop
    """
    global isSuspended
    global isStop
    global volumeTotal

    #Prelevement : Isolate Cells, Remove x ml from circuit, Pause cycle
    if actionToDo == "Sample":
        isSuspended = True
        volumeTotal = volumeTotal-int(argument)
        for vanne in listeVanne:
            if vanne.id=="cells":
                vanne.off()
        with Tee():
                print(getTime()+"|"+"You can take your sample")
    #Observation : Isolate Cells, Pause cycle
    elif actionToDo == "Observation":
        isSuspended = True
        for vanne in listeVanne:
            if vanne.id=="cells":
                vanne.off()
        with Tee():
                print(getTime()+"|"+"You can do your observation")
    #Reprendre cycle : Open cells, restart cycle
    elif actionToDo == "Resume_cycle":
        isSuspended = False
        for vanne in listeVanne:
            if vanne.id=="cells":
                vanne.on()
        with Tee():
                print(getTime()+"|"+"Restarting cycle")
    #Stop script
    elif  actionToDo == "Stop":
        isStop = True

def getConc():
    """
    Get concentratoion from ftr file
    """
    global startTime
    timeInSecond = int((time.monotonic()-startTime))
    conc1 = concentrationFile["Conc1"].iloc[timeInSecond]
    conc2 = concentrationFile["Conc2"].iloc[timeInSecond]
    nutConc = 100.0 - conc1 - conc2
    nutConc = nutConc / 100
    conc1 = conc1 / 100
    conc2 = conc2 / 100
    return nutConc,conc1,conc2

def startPurge(purgeTime):
    """
    Purge the system
    """
    for vanne in listeVanne:
        vanne.on()

    with Tee():
        print(getTime()+"|"+"Starting purge")

    time.sleep(purgeTime)

    with Tee():
        print(getTime()+"|"+"Purge finished")

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
    add=[0.0,0.0,0.0]
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

    if isStop:
        pass
    else:
        scheduleConcentration = threading.Timer(timeBetweenChange * 60, changeConcentration)
        scheduleConcentration.start()

    if isSuspended:
        if scheduleConcentration is not None and scheduleConcentration.is_alive():
            scheduleConcentration.cancel()
    else:
        with Tee():
            print(getTime()+"|"+"Starting new concentration cycle, actual volume : "+str(round(volumeTotal,1))+" ml")
        nutConc,conc1,conc2 = getConc()
        
        with Tee():
            print(getTime()+"|"+"Target concentration : nutriment : "+str(nutConc*100)+", Hormone 1 : "+str(conc1*100)+", Hormone 2 : "+str(conc2*100))

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
            with Tee():
                print(getTime()+"|"+"Purge needed : "+str(volumePurge)+" ml")
            startPurge(timePurge)
            volumeTotal = volumeTotal-volumePurge
        
        with Tee():
            print(getTime()+"|"+"Injection nutriment : "+str(volInjection[0])+" ml")

        for vanne in listeVanne:
            if vanne.id == "purge" or vanne.id=="cells":
                vanne.off()
            else:
                vanne.on()

        time.sleep(timeNut)
        volumeTotal = volumeTotal+volInjection[0]


        for vanne in listeVanne:
            vanne.off()

        with Tee():
            print(getTime()+"|"+"Injection hormmones : Hormone 1 :"+str(volInjection[1])+" ml, Hormone 2 : "+str(volInjection[2])+" ml")

        for pump in listePompe:
            if pump.id == "conc1":
                pump.injection(volInjection[1])
            if pump.id == "conc2":
                pump.injection(volInjection[2])
        volumeTotal = volumeTotal+volInjection[1]+volInjection[2]
        time.sleep(30)

        for vanne in listeVanne:
            if vanne.id == "cells":
                vanne.on()
            else:
                vanne.off()
        with Tee():
            print(getTime()+"|"+"New concentration achieved, New volume : "+str(round(volumeTotal,1))+" ml")



def setupGPIO():
    """
    Setup GPIO for control
    """
    GPIO.setmode(GPIO.BCM)

    #Moteur
    GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
    
    #Electrovanne
    GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(6, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)

checkOs()
if getArg():
    setupGPIO()
    for pump in listePompe:
        if pump.id == "flow":
            pump.on()
        else:
            pass
    startTime = time.monotonic()
    changeConcentration()
    while not isStop:
        if getFirstLine() != "":
            actionToDo, argument = prepareAction(getFirstLine())
            with Tee():
                print(getTime()+"|"+"action : "+str(actionToDo))
            doAction(actionToDo, argument)
            removeLine()

    if scheduleConcentration is not None and scheduleConcentration.is_alive():
        scheduleConcentration.cancel()
    with Tee():
        for pump in listePompe:
            pump.off()
        for vanne in listeVanne:
            vanne.off()
        print(getTime()+"|"+"Experience stop")
else:
    pass
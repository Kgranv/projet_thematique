# Requirements :<br/>

## For Raspberry pi

- Raspberry Pi OS Lite (64-bit)
- Python 3.10
- Python Libraries :
  - numpy 1.22.2
  - pandas 1.4.1
  - feather-format 0.4.1

## For Windows (optional)

- Python 3.10
- Python Libraries :
  - numpy 1.22.2
  - pandas 1.4.1
  - feather-format 0.4.1
  - matplotlib 3.5.2

# RaspberryPi recommendation :<br/>

- RaspberryPi type : RaspberryPi-4 <br/>
- RaspberryPi name : raspberrypi-projetMOON <br/>
- piUser : projetMOON <br/>

# Useful command :<br/>

For windows with powershell :<br/>

- Connect to raspberryPi with SSH :<br/>
  <code>ssh piUser@piName</code><br/>
- Send file to raspberryPi :<br/>
  <code>scp dataToSend piUser@piName:/home/piUser/folderPath</code><br/>
- Retrieve file from raspberryPi :<br/>
  <code>scp piUser@piName:/home/piUser/FilePath localFilePath</code><br/>
  if you are already in localFilePath, replace localFilePath by ".\\"<br/>

For raspberry-pi terminal :<br/>

- View file in directory :<br/>
  <code>ls</code><br/>
- change directory :<br/>
  <code>cd directoryName</code><br/>
  if you want to go in parent folder change directoryName by ..
- remove file :<br/>
  <code>rm fileName</code><br/>
- read file :<br/>
  <code>cat fileToRead</code>
- start pyhton script<br/>
  <code>python script.py</code><br/>
- start experience script<br/>
  <code>nohup python experience.py ftrFile.ftr</code><br/>

# How to setup your raspberry-pi :<br/>

You need to use the Raspberry Pi Imager software available here : https://www.raspberrypi.com/software/<br/>
![PiImagerPicture1](/imgReadMe/PiImager1.png)

## Step 1 : Chose OS

You need to chose the Raspberry Pi OS Lite(64-bit). Don't use 32-bit OS because some library needs a 64-bit OS.<br/>
You can find it in Raspberry Pi OS (other) menu.
![PiImagerPicture2](/imgReadMe/PiImager2.png)
![PiImagerPicture3](/imgReadMe/PiImager3.png)

## Step 2 : Chose storage

Select the SD card you will use for the raspberry pi.

## Step 3 : Setup advance parameter

You need to change multiple parameter before writing the OS in the SD card :<br/>
You can find the parameter in the gear.<br/>

- Chose for all sessions in Image customization options
- Change the raspberry pi name<br/>
- Activate SSH : <br/>
  use authentification by password<br/>
- Define username and password<br/>
- Configurate the wifi<br/>

![PiImagerPicture4](/imgReadMe/PiImager4.png)
![PiImagerPicture5](/imgReadMe/PiImager5.png)
![PiImagerPicture6](/imgReadMe/PiImager6.png)

## Step 4 : Write on SD card

You can write the OS in the SD card and your OS it's ready !<br/>

## Step 5 : Install dependencies and Setup directory

You need to install dependencies.<br/>

- Connect to your raspberry pi via SSH :<br/>
  <code>ssh piUser@piName</code><br/>
  use the piUser and piName you have setup in step 3.<br/>
- Install OS update :<br/>
  <code>sudo apt update</code><br/>
  <code>sudo apt upgrade</code><br/>
- Install python :<br/>
  <code>sudo apt install python3.10</code>
- Install python library :<br/>
  <code>pip install numpy</code><br/>
  <code>pip install pandas</code><br/>
  <code>pip install feather-format</code><br/>
- Create directory :<br/>
  <code>mkdir data</code><br/>
  <code>mkdir userData</code><br/>

All the dependencies are installed you can close the SSH connection by closing the terminal.<br/>

## Step 6 : Transfert file on raspberry pi

You need to transfert all necessary file on raspberry pi.<br/>
Download following file from the repository :<br/>

- armerPompe.py<br/>
- controle.csv<br/>
- controle.py<br/>
- dataPreparation.py<br/>
- experience.py<br/>
- resetGPIO.py<br/>

repeat the following command for each file in the list to transfert to raspberry pi :<br/>

- Send file to raspberryPi :<br/>
  <code>scp fileToSend piUser@piName:/home/piUser</code><br/>

The setup of the raspberry pi is complete.

# Plug experience

## Motor

### Motor n°1

- red wire to Mosfet 1 Drain
- black wire to Mosfet 1 Source

### Motor n°2

- red wire to Mosfet 2 Drain
- black wire to Mosfet 2 Source

### Motor n°3

- red wire to Mosfet 3 Drain
- black wire to Mosfet 3 Source

## Electrovanne

### Electrovanne n°1

- wires to Mosfet 4 Drain/Source

### Electrovanne n°2

- wires to Mosfet 5 Drain/Source

### Electrovanne n°3

- wires to Mosfet 5 Drain/Source

## Raspberry pin

### Alimentation

- pin 4 (Alimentation 5V) to 5 V
- pin 6 (GND) to GND

### Motor

- pin 11 (GPIO 17) to Mosfet 1 Gate
- pin 13 (GPIO 27) to Mosfet 2 Gate
- pin 15 (GPIO 22) to Mosfet 3 Gate

### Electrovanne

- pin 29 (GPIO 5) to Mosfet 4 Gate
- pin 31 (GPIO 6) to Mosfet 5 Gate
- pin 33 (GPIO 13) to Mosfet 6 Gate

# Run an experience

## Step 1 : Prepare your data

The data need to be in csv file. The separator need to be ",".<br/>
Your data are presented like this :<br/>

| time | conc1 | conc2 |
| :--- | :---- | :---- |
| 0    | 1     | 1     |
| 2    | 6     | 8     |
| 10   | 2     | 1     |
| 15   | 4     | 2     |

time correspond of time from the start in second.<br/>
conc1 and conc2 it's the concentration of element at time t.

If you have download dataPreparation.py on your computer you can convert your data on your computer directly.
For convert your data directly on your computer follow the Step 3 before the Step 2.

## Step 2 : Transfert your data on raspberry pi

Transfert your data on the raspberry pi in the folder userData.<br/>
Open terminal in the folder of your data and use this command :<br/>
<code>scp dataToSend piUser@piName:/home/piUser/userData</code><br/>

If you have convert your data directly on your computer use this command instead :<br/>
<code>scp dataToSend piUser@piName:/home/piUser/data</code><br/>

## Step 3 : Convert your data

### If you have transfert your CSV file on raspberry pi

- Connect to your raspberry pi via SSH :<br/>
  <code>ssh piUser@piName</code><br/>
- run dataPreparation.py :<br/>
  <code>python dataPreparation.py</code><br/>
  Indicate the name of your data when ask.

Your data is now converted and placed in data.<br/>
The data converted is named by the date of creation like this:<br/>
year-moth-day_hourminsec.ftr

you can check the name of the data created in the folder data using :<br/>
<code>cd data</code><br/>
<code>ls</code><br/>
it will show all the data in the folder data.<br/>

### If you want convert your data on Windows

Before convert your data on Windows make sure you have the optionnal requirement on your computer.<br/>
Create 2 folder in directory of dataPreparation.py:<br/>

- userData<br/>
- data<br/>

Put your data to convert in userData folder.<br/>
Run dataPrepartion.py and indicate the name of your data when ask.<br/>
Your data is now converted and placed in data.<br/>
The data converted is named by the date of creation like this:<br/>
year-moth-day_hourminsec.ftr<br/>
You can check the data created using the script verificationFtr.py<br/>
Now you can do Step 2.

## Step 4 : Run experience

For start experience connect to raspberry pi if it's not already done :<br/>
<code>ssh piUser@piName</code><br/>
Run experience.py in background with :<br/>
<code>nohup python experience.py dataToUse.ftr</code><br/>
Close the terminal.<br/>
The Experience is running Step 5 and 6 will show you how to interact with experience.

## Step 5 : Control experience

If you want take sample or make an observation during the experience you need to suspend the process.

- Connect to raspberry pi :<br/>
  <code>ssh piUser@piName</code><br/>
- run controle.py
  <code>python controle.py</code><br/>
- Chose what you want to do :<br/>
  1. Sample<br/>
     For take a sample, you need to indicate which quantity you take.<br/>
  2. Observation<br/>
     For observe the cells.<br/>
  3. Restart cycle<br/>
     When you have finished your sample/observation restart the cycle.<br/>
  4. Log<br/>
     For see the last log of the experience.<br/>
  5. Stop<br/>
     Force stop of the experience if something goes wrong.<br/>
  6. Cancel<br/>
     Close controle.py<br/>

When you have finished dont forget to restart cycle and you can press cancel for close controle.py.<br/>

## Step 6 : Check log

- Connect to raspberry pi :<br/>
  <code>ssh piUser@piName</code><br/>
- Open the log:<br/>
  <code>cat output.log</code><br/>

For debug log use instead :<br/>
<code>cat nohup.out</code><br/>

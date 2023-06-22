# Requirements :<br/>

## For Raspberry pi

- OS :
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

# RaspberryPi info :<br/>

- RaspberryPi type : RaspberryPi-4
  <br/>
- RaspberryPi name : raspberrypi-zero-MOON
- piUser : projetMOON

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
  <code>pip install numpy</code>
  <code>pip install pandas</code>
  <code>pip install feather-format</code>
- Create directory :<br/>
  <code>mkdir data</code>
  <code>mkdir userData</code>

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

Your data is now converted.<br/>
The data converted is named by the date of creation like this:<br/>
year-moth-day_hourminsec.ftr

### If you want convert your data on Windows

Before convert your data on Windows make sure you have the optionnal requirement on your computer.<br/>
Create 2 folder in directory of dataPreparation.py:

- userData<br/>
- data<br/>

Put your data to convert in userData folder.<br/>
Run dataPrepartion.py and indicate the name of your data when ask.<br/>
Your data is now converted.<br/>
The data converted is named by the date of creation like this:<br/>
year-moth-day_hourminsec.ftr<br/>
You can check the data created using the script verificationFtr.py

## Step 4 : Run experience

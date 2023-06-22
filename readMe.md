# Requirements :<br/>

- OS :
  - Raspberry Pi OS Lite (64-bit)
- Python Libraries :
  - numpy 1.22.2
  - pandas 1.4.1
  - feather-format 0.4.1

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

You can write the OS in the SD card and it's ready !<br/>

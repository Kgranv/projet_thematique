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

- Connect to raspberryPi with SSH
  <code>ssh piUser@piName</code><br/>
- Send file to raspberryPi :<br/>
  <code>scp dataToSend piUser@piName:/home/piUser/folderPath</code><br/>
- Retrieve file from raspberryPi :<br/>
  <code>scp piUser@piName:/home/piUser/FilePath LocalFilePath</code><br/>
  if you are already in LocalFilePath, replace LocalFilePath by ".\\"<br/>

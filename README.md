# kindle-keyboard-mqtt-client
A simple python program that allows you to use your old Kindle 3 to control events in HomeAsistant - press of a kindle keyboard button is sent as event over mqtt. 

This works as great addition to this project - https://github.com/sibbl/hass-lovelace-kindle-screensaver ; So kindle will show the dashboard and you can use also buttons to control stuff.

Prerequisites : 
a) Kindle 3 with jailbreak (Kindle 4 or other kindles with buttons will possibly work) - Jailbreak resources here https://kindlemodding.org/jailbreaking/Legacy/K2DXDXGK3-Jailbreak/
b) Python 3 installed on kindle (https://www.mobileread.com/forums/showthread.php?t=225030)

How to : 
1) Install Mosquitto for your HomeAsistant if you already dont have them installed.
2) Add integration MQTT
3) Create a new login for mosquitto - or use the one generated during install.
4) Log into your kindle with SSH.
5) paho-mqtt library for python3 needs to be installed on your kindle. Your kindle doesnt have pip so you have to install it by copying the files manually.
6) disable sleep on your kindle if you havent already done that - either through ssh command or there is a way through the kindle itself (sleep interferes with this script)
7) edit the python script with nano and change your homeasistant IP and mosquitto broker logins
6) copy the file somewhere to /mnt/us/hass-kkmc - either with nano or use Winscp or other tool.
7) start it with "python3 /mnt/us/hass-kkmc/hass-kindle-mqtt-client0.1.py&
8) now a new device is created in your homeasistant under integrations/mqtt click on it and you can create automations from there 

If you want this to autostart just add it to cron

<img width="400" height="711" alt="VID_20260605_171555044(1)" src="https://github.com/user-attachments/assets/da598a6c-3573-4007-ab38-00e2f8040f6a" />


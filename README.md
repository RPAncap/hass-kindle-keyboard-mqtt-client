# kindle-keyboard-mqtt-client
A simple python program that allows you to use your old Kindle 3 to control events in HomeAsistant - press of a kindle keyboard button is sent as event over mqtt. It also adds to functionality to play .wav files through Kindle speakers.

This works as great addition to this project - https://github.com/sibbl/hass-lovelace-kindle-screensaver ; So kindle will show the dashboard and you can use also buttons to control stuff.

This will likely work on other Kindles that have buttons (such as Kindle 2 or Kindle 4) with slight modifications - I do not have one of those to try - if you do feel free to test and contact me and I can add it here.

Prerequisites : 
1) Kindle 3 with jailbreak (Kindle 4 or other kindles with buttons will possibly work) - Jailbreak resources here https://kindlemodding.org/jailbreaking/Legacy/K2DXDXGK3-Jailbreak/
2) Python 3 installed on kindle (https://www.mobileread.com/forums/showthread.php?t=225030)

How to Install : 
1) Install Mosquitto for your HomeAsistant if you already dont have them installed.
2) Add integration MQTT
3) Create a new login for mosquitto - or use the one generated during install.
4) Log into your kindle with SSH.
5) paho-mqtt library for python3 needs to be installed on your kindle. Your kindle doesnt have pip so you have to install it by copying the files manually.
6) Disable sleep on your kindle if you havent already done that - either through ssh command or there is a way through the kindle itself (sleep interferes with this script)
7) Edit the python script with nano and change your homeasistant IP and mosquitto broker logins
6) Copy the files somewhere f.e. /mnt/us/kkmc - use WinSCP or other tool.
7) Start it with "python3 /mnt/us/kkmc/kindle-keyboard-mqtt-client.py > out.log &"
8) Now a new device is created in your homeasistant under integrations/mqtt click on it and you can create automations from there. 

If you want this to autostart just add it to cron

Using the kindle to play sounds : 
For simplicity we are using the native tool aplay that is preinstalled in kindle. It can only play .wav files. Place your .wav files in the same folder and name tham 1.wav 2.wav and so on (by default there is 1-4 but you can edit the configurations at the start of the code and add more or name hovewer you want).
In integrations / mqtt you will see the Kindle device and when you click it there are the buttons corresponding to your .wav files.


<img width="400" height="711" alt="VID_20260605_171555044" src="https://github.com/user-attachments/assets/5d5754f2-d728-4e50-baa1-364a2c22e572" />

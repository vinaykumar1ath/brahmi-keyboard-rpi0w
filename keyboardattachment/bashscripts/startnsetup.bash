#!/bin/bash

cd /home/pi

sudo apt update

sudo apt upgrade

sudo apt install python3-pip

pip3 install keyboard

cd /home/pi/keyboardattachment/main

sudo chmod +x mainstarter

cd /home/pi/keyboardattachment/bashscripts

sudo chmod +x installer.bash

sudo ./installer.bash

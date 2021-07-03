#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd /home/pi/myWorkspace/python_programs/MedicineReminder
sudo python MedicineReminder.py
cd /

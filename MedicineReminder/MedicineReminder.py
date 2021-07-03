# -*- coding: utf-8 -*-
import wave
import sys
import threading
import time
import RPi.GPIO as GPIO
from subprocess import Popen


# Mapping Table/Dictionary for the "time of reminder" and the
# "reminder voice content file to be played"
# Actual Field Values
# Last value @ 00:00 is for testing
reminder = {'09:00':'sartel40Reminder.wav',
            '21:00':'nebula2pt5Reminder.wav'}

def playWavFileUsingaplay(wavFile):
    logToFile("\nEntering playWavFileUsingaplay() function !....")
    wavFile = '/home/pi/myWorkspace/python_programs/MedicineReminder/' + wavFile
    Popen(['aplay', wavFile])
    logToFile("\nExiting playWavFileUsingaplay() function !")

def scheduleTimer():
    logToFile("\nEntering scheduleTimer() function!")
    timer = threading.Timer(30, timerCallback) 
    timer.start()
    logToFile("\nExiting scheduleTimer() function!")

def timerCallback():
    global reminderNotification
    global wavFileGlobal
    
    logToFile("\nEntering timerCallback() function : Timer Expired!....")
    currentTime = time.ctime()
    timer = threading.Timer(30, timerCallback) 
    timer.start()
    logToFile("\nNew 30 Sec Timer Started")    

    reminderTimeHit = reminder.get(currentTime[11:16], 'No')
    if(reminderTimeHit != 'No'):
        # New time/reminder hit
        logToFile("\nNotification Condition Hit !")
        reminderNotification = True
        wavFileGlobal = reminderTimeHit
        logToFile(wavFileGlobal)
        
    if(reminderNotification):
        logToFile("\nReminder : Every 30 sec")
        logToFile(wavFileGlobal)
        playWavFileUsingaplay(wavFileGlobal)
        logToFile("\nWave File Played!")

def button_callback(channel):
    global reminderNotification
    global pinValueEqualsZeroCounter
    global debounceInProgress
    
    logToFile("Entering button_callback() function.......")

    # Get value on the given pin number
    pinValue = GPIO.input(18)

    if(pinValue == 0):
        pinValueEqualsZeroCounter += 1
        
    if((debounceInProgress == False) and (pinValue == False)):
        debounceInProgress = True
        # Debounce interval set 200 ms
        switchDebounce(18, 0.2)

    logToFile("Exiting button_callback() function.......")

def switchDebounce(pinNum, debounceInterval):
    logToFile("Entering switchDebounce() function.......")
    # Start debouce timer
    debounceTimer = threading.Timer(debounceInterval, debounceTimerCallback) 
    debounceTimer.start()
    logToFile("Exiting switchDebounce() function.......")

def debounceTimerCallback():
    global pinValueEqualsZeroCounter
    global reminderNotification
    global debounceInProgress

    logToFile("Entering debounceTimerCallback() function.......")
    
    # Get value on the given pin number
    pinValue = GPIO.input(18)
    # Check if the first reading is same as the reading
    # after debounce interval
    if((pinValueEqualsZeroCounter >= 3) or (pinValue == 0)):
        pinValueEqualsZeroCounter = 0
        # Switch genuinely pressed
        reminderNotification = False
        logToFile("Multiple hits to the required key press value detected: Button Pressed!")
    
    logToFile("Exiting debounceTimerCallback() function.......")
    debounceInProgress = False

def init():
    global reminderNotification
    global wavFileGlobal
    global debounceInProgress
    global pinValueEqualsZeroCounter
    
    reminderNotification = False
    wavFileGlobal = 'sartel40Reminder.wav'
    debounceInProgress = False
    pinValueEqualsZeroCounter = 0
    
    # Each pin on the Raspberry Pi has several different names, so you need to tell the program
    # which naming convention is to be used.
    GPIO.setmode(GPIO.BCM)
    
    # This tells Python not to print GPIO warning messages to the screen.    
    GPIO.setwarnings(False)
    
    # This line tells the Python interpreter that pin 18 is going to be used for outputting information,
    # which means you are going to be able to turn the pin ‘on’ and ‘off’.
    # Set pin 18 to be an input pin and set initial value to be pulled HIGH (ON)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Setup event on pin 18 falling edge
    GPIO.add_event_detect(18,GPIO.FALLING,callback=button_callback)

def logToFile(logText):
    logData = True
    if(logData):
        f1=open('/home/pi/myWorkspace/python_programs/MedicineReminder/Log.txt', 'a')
        # Log the current time
        f1.write(time.ctime())
        f1.write('\n')
        f1.write(logText)
        f1.close()

def test():
    # 2 min in future
    estimatedHr = str(time.localtime(time.time() + 120).tm_hour)
    if(len(estimatedHr) == 1):
        estimatedHr = '0' + estimatedHr
    
    estimatedMin = str(time.localtime(time.time() + 120).tm_min)
    if(len(estimatedMin) == 1):
        estimatedMin = '0' + estimatedMin
    
    reminder[estimatedHr + ':' + estimatedMin] = 'nebula2pt5Reminder.wav'
    logToFile(str(reminder))


# Start of program execution
init()
# test()
scheduleTimer()

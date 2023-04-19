import json
import sys
import shutil
from flask import Flask, jsonify
from flask import request as flaskRequest
from csv import writer
from flask import render_template
import mysql.connector
import RPi.GPIO as GPIO
import time
import numpy as np


app = Flask('app')

# INTIALIZE GPIO-PINS =================================================
# Declare the channels for each device

TRIG = 16 #Ultrasound projector
ECHO = 15 #Ultrasound Receiver
solenoid = 12 #solenoid
# GreenLED = 11 #Green LED

# INTIALIZE VARIABLES =================================================

timeElapsed = 0
threshold = 25 # distance in centimeters
T = np.array([])
D = np.array([])

# DEFINE FUNCTIONS ====================================================
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up GPIO mode and define input and output pins

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(solenoid, GPIO.OUT)
    # GPIO.setup(GreenLED, GPIO.OUT)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function given by SunFounder to calculate distance from sensor

def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    
    while GPIO.input(ECHO) == 0:
        time1 = time.time()
        
    while GPIO.input(ECHO) == 1:
        time2 = time.time()

    during = time2 - time1
    return during * 340 / 2 * 100 #Returns distance in cm



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                
# WRITE DATA TO ARRAYS, PRINT DATA ON TERMINAL for 10 seconds

def loop():


        global timeElapsed, T, D
        
        while timeElapsed <= 10:
            # writes the time elapsed and distance measured
            # Turns LED to RED if object within 'threshold' distance
            dist = distance()

            print(timeElapsed, 's', dist, 'cm')
            print('')

            time.sleep(0.1)
            timeElapsed = timeElapsed+0.1
            
            D = np.append(D, dist)
            T = np.append(T, timeElapsed)
            
            global threshold
            if(dist<threshold):
                GPIO.output(11, GPIO.LOW)
                GPIO.output(12, GPIO.HIGH)
            else:
                GPIO.output(11, GPIO.HIGH)
                GPIO.output(12, GPIO.LOW)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



@app.route('/checkAlarm', methods=['POST'])
def checkAlarm(audio):
    data = flaskRequest.get_json()
    print(data)


    # Check if correct ringtone (forrier transform)
    # If not correct:
    # return

    # If correct:
    madeCofee = makeCoffee()

    # If not madeCoffee:
    # return

    # If madeCoffee:
    timeToTakeCoffee()

    return ""



def makeCoffee():
    setup()
    # First, check how long we should wait until making the coffee
    # Wait until set time

    # Second, check ultrasound sensor for cup
    loop()
    # If not cup:
    # return false

    # If cup:
    # Activate actuator to press button
    # return true

    return

def timeToTakeCoffee():
    return


makeCoffee()





app.run(host='0.0.0.0', port=8080)
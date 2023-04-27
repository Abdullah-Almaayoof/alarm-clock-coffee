import json
import sys
import shutil
# import mysql.connector
import RPi.GPIO as GPIO
import time
from time import sleep
import numpy as np
import math
import wave
import os
import struct
#import matplotlib.pyplot as plt
#from scipy.io.wavfile import write
#import soundfile as sf
import soundfile as sf
import simpleaudio
import pyaudio
import requests

count = 0

def recordAudio():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 30
    global count
    filename = "stream.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    # 
    print('Recording')
    # 
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk, exception_on_overflow = False)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()



# INTIALIZE GPIO-PINS =================================================
# Declare the channels for each device

TRIG = 16 #Ultrasound projector
ECHO = 20 #Ultrasound Receiver
solenoid = 12 #solenoid
GreenLED = 11 #Green LED

# INTIALIZE VARIABLES =================================================

timeElapsed = 0
threshold = 25 # distance in centimeters
T = np.array([])
D = np.array([])

# DEFINE FUNCTIONS ====================================================
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up GPIO mode and define input and output pins

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(solenoid, GPIO.OUT)
    GPIO.setup(GreenLED, GPIO.OUT)

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
                return True
                # GPIO.output(11, GPIO.LOW)
                # GPIO.output(12, GPIO.HIGH)
            else:
                return False
                # GPIO.output(11, GPIO.HIGH)
                # GPIO.output(12, GPIO.LOW)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# @app.route('/checkAlarm', methods=['POST'])
# def checkAlarm(audio):
#     data = flaskRequest.get_json()
#     print(data)


#     # Check if correct ringtone (forrier transform)
#     # If not correct:
#     # return

#     # If correct:
#     madeCoffee = makeCoffee()

#     print("\nMade Coffee? ", madeCoffee)

#     # If not madeCoffee:
#     # return

#     # If madeCoffee:
#     timeToTakeCoffee()

#     return ""


def sendAudioLoop():
    run = False
    print('running client')
    runCount = 0
    global count
    lastResult = 'False'
    while run == False:
        url = 'http://128.164.208.163:8080/recieveAudio'
        file = {'file': open(r'stream.wav', 'rb')}
        try:
            requests.post(url, files=file, timeout=1)
        except:
            url = 'http://128.164.208.163:8080/getRunCount'
            currentCount = requests.get(url).content
            print(currentCount.decode('UTF-8'))
            url = 'http://128.164.208.163:8080/getLastRun'
            lastResult = requests.get(url).content
            print(lastResult.decode('UTF-8'))
            if 'True' in lastResult.decode('UTF-8'):
                run = True
            recordAudio()
        count+=1
        
        
    print('ALARM DETECTED')
    makeCoffee()
    return
                

def makeCoffee():
    global timeElapsed, T, D

    setup()
    # First, check how long we should wait until making the coffee
    # Wait until set time

    # Second, check ultrasound sensor for cup
    cup = loop()
    if not cup:
        print("\nCup not available\n")
        return False
    else:
        print("\nCup available, will make coffee now\n")
#        while timeElapsed <= 1:
#            time.sleep(0.1)
#            timeElapsed = timeElapsed+0.1
#
#            GPIO.output(11, GPIO.LOW)
#            GPIO.output(12, GPIO.HIGH)
#            sleep(1)
#            GPIO.output(11, GPIO.HIGH)
#            GPIO.output(12, GPIO.LOW)
        GPIO.setup(24, GPIO.OUT)
        GPIO.setup(25, GPIO.OUT)
    
    
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(25, GPIO.HIGH)
        sleep(0.1)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(25, GPIO.LOW)

        return True

def timeToTakeCoffee():
    return

sendAudioLoop()

#setup()
#GPIO.setmode(GPIO.BCM)

#makeCoffee()
#GPIO.setup(24, GPIO.OUT)
#GPIO.setup(25, GPIO.OUT)
#
#
#GPIO.output(24, GPIO.HIGH)
#GPIO.output(25, GPIO.HIGH)
#sleep(0.1)
#GPIO.output(24, GPIO.LOW)
#GPIO.output(25, GPIO.LOW)
GPIO.cleanup()
#









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
from temp import *

import signal

GPIO.setwarnings(False)

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)


count = 0

def recordAudio():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 10
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
threshold = 10 # distance in centimeters
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

    time2 = 0
    time1 = 0
    while GPIO.input(ECHO) == 0:
        time1 = time.time()
        
    while GPIO.input(ECHO) == 1:
        time2 = time.time()
    if time2 == 0 or time2 == 0:
        return -1
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
            if dist < 0:
                print('-1')
#            print(timeElapsed, 's', dist, 'cm')
#            print('')

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

def revLoop():
        global timeElapsed, T, D
        
        # writes the time elapsed and distance measured
        # Turns LED to RED if object within 'threshold' distance
        dist = distance()

#        print(timeElapsed, 's', dist, '')
#        print('')

        time.sleep(0.1)
        timeElapsed = timeElapsed+0.1
        
        D = np.append(D, dist)
        T = np.append(T, timeElapsed)
        
        global threshold
        if(dist<threshold):
            return False
        else:
            return True

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
        url = 'http://192.168.1.153:8080/recieveAudio/'+str(1+count)
        file = {'file': open(r'stream.wav', 'rb')}
        try:
            requests.post(url, files=file, timeout=1)
        except:
            url = 'http://192.168.1.153:8080/getRunCount'
            currentCount = requests.get(url).content
            print(currentCount.decode('UTF-8'))
            url = 'http://192.168.1.153:8080/getLastRun'
            lastResult = requests.get(url).content
            print(lastResult.decode('UTF-8'))
            if 'True' in lastResult.decode('UTF-8'):
                run = True
            recordAudio()
        count+=1
        
        
    print('ALARM DETECTED')
    makeCoffee()
                

def makeCoffee():
    global timeElapsed, T, D
    
    setup()
    # First, check how long we should wait until making the coffee
    avg_wait_time = get_average_wait_time()
    print('waitng '+str(avg_wait_time)+' seconds')
    # Wait until set time
    time.sleep(avg_wait_time)

    # Second, check ultrasound sensor for cup
    cup = loop()
    if not cup:
        print("\nCup not available\n")
        return False
    else:
        print('---------------------------------------')
        print("\nCup available, will make coffee now\n")
        print('---------------------------------------')

        start_time = time.time()
        GPIO.setup(24, GPIO.OUT)
        GPIO.setup(25, GPIO.OUT)
        for i in range(3):
            GPIO.output(24, GPIO.HIGH)
            GPIO.output(25, GPIO.HIGH)
            sleep(1)
            GPIO.output(24, GPIO.LOW)
            GPIO.output(25, GPIO.LOW)

        seconds = 0
        while not revLoop() and seconds < 30:
            sleep(1)
            seconds+=1
        if not loop():
            end_time = time.time()
            elapsed_time = end_time - start_time
            print('time elapsed: '+str(elapsed_time)+'s')
            write_time_to_csv(elapsed_time)
            return True
            
        print('sending data to dweet.io')
        sendTemp()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print('time elapsed: '+str(elapsed_time)+'s')
        write_time_to_csv(elapsed_time)
            
        return True


def timeToTakeCoffee():
    start_time = time.time()
    while not revLoop():
        pass
    end_time = time.time()
    elapsed_time = end_time - start_time
    if elapsed_time > 60*10:
        elapsed_time = 60*10
    write_time_to_csv(elapsed_time)


def write_time_to_csv(time_elapsed):
    with open('coffee_time.csv', 'r') as f:
        lines = f.readlines()
        if len(lines) < 7:
            lines.append(str(time_elapsed) + '\n')
        else:
            lines.pop(0)
            lines.append(str(time_elapsed) + '\n')
    with open('coffee_time.csv', 'w') as f:
        f.writelines(lines)

def get_average_wait_time():
    try:
        with open('coffee_time.csv', 'r') as f:
            lines = f.readlines()
        times = [float(line.strip()) for line in lines]
        avg_time = sum(times) / len(times)
        return avg_time
    except:
        return 0
        

def sendTemp():
    print('sending temp while mug is there')
    while not revLoop():
        signal.alarm(1)
        try:
            quality = checkTemp()
        except TimeoutException:
            print('temperature timeout')
            continue 
        else:
            signal.alarm(0)

        if quality != False:
            humidity, temperature = quality
            coffeeTemp = estimate_coffee_temperature(temperature, humidity)
            try:
                url = 'https://dweet.io/dweet/for/csci3907coffeeTemp'
                myobj = {'temperature': coffeeTemp}
                x = requests.post(url, json = myobj, timeout = 1)
            
                print(x.text)
            except:
                print("Waiting for connection")
            
            time.sleep(1)





def estimate_coffee_temperature(temp, humidity):
    # Calculate the dew point temperature
    a = 17.27
    b = 237.7
    alpha = ((a * temp) / (b + temp)) + math.log(humidity/100.0)
    dew_point = (b * alpha) / (a - alpha)
    # Estimate the coffee temperature assuming the dew point temperature is the same as the coffee temperature
    coffee_temp = (temp - dew_point) * 1.15 + dew_point
    return coffee_temp

GPIO.cleanup()

#sendAudioLoop()
#quality = False
#while quality == False:
#    quality = checkTemp()
#humidity, temperature = quality
#dew = temperature-((100-humidity)/5)
#print(dew)
sleep(5)
makeCoffee()

GPIO.cleanup()









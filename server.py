import json
import sys
import shutil
from flask import Flask, jsonify
from flask import request as flaskRequest
from csv import writer
from flask import render_template
# import mysql.connector
import time
from time import sleep
import numpy as np
import os
import alarm as alarm


app = Flask('app')

@app.route('/test', methods=['GET'])
def test():
    return 'test'

lastRun = 'False'
runCount = 0

@app.route('/getLastRun', methods=['GET'])
def getLastRun():
    global lastRun
    return lastRun

@app.route('/getRunCount', methods=['GET'])
def getRunCount():
    global runCount
    return str(runCount)


@app.route('/recieveAudio', methods=['GET', 'POST'])
def upload():
    global runCount
    global lastRun
    if flaskRequest.method == 'POST':
        file = flaskRequest.files['file']
        if file:
            filename = 'stream.wav'
            print(filename)
            new_filename = f'{filename.split(".")[0]}.wav'
            save_location = os.path.join('input', new_filename)
            file.save('stream.wav')
            
            #return send_from_directory('output', output_file)
            if alarm.checkAlarmSegment('stream.wav'):
                print('returning True')
                lastRun = 'True'
            else:
                print('returning False')
                lastRun = 'False'
        else:
            lastRun = 'No File'
        runCount +=1
        return ''

    lastRun = 'Not a Post Request'
    return ''




app.run(host='0.0.0.0', port=8080)
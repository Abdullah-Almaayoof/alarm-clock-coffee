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

@app.route('/recieveAudio', methods=['GET', 'POST'])
def upload():
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
                return 'True'
            else:
                print('returning False')
                return 'False'
        else:
            return 'No file'

    return 'Not Post'




app.run(host='0.0.0.0', port=8080)
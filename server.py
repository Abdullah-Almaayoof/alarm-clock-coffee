import json
import sys
import shutil
from flask import Flask, jsonify
from flask import request as flaskRequest
from csv import writer
from flask import render_template
import mysql.connector

app = Flask('app')


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
    # First, check how long we should wait until making the coffee
    # Wait until set time

    # Second, check ultrasound sensor for cup
    # If not cup:
    # return false

    # If cup:
    # Activate actuator to press button
    # return true

    return

def timeToTakeCoffee():
    return





app.run(host='0.0.0.0', port=8080)
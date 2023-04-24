import requests

url = 'http://127.0.0.1:8080/upload'
file = {'file': open(r'C:\Users\S-_-z\OneDrive\Documents\GitHub\alarm-clock-coffee\alarm_mono_single.wav', 'rb')}
response = requests.post(url, files=file)
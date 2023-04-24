import wave
import os
import struct
# import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf
# import simpleaudio
import pyaudio
# import speech_recognition as sr
import requests
from sklearn.metrics import mean_squared_error
import librosa
import pandas as pd
from librosa import display

import matplotlib.pyplot as plt

import numpy as np
from scipy.fftpack import fft
def soundFFT(filename):
  samples, sampling_rate = librosa.load(filename, sr = None, mono = True, offset = 0, duration = None)
  print(len(samples), sampling_rate, len(samples)/sampling_rate)
  n = (len(samples))
  T = 1/sampling_rate
  yf = fft(samples)
  xf = np.linspace(0.0, 1.0/(2.0*T), (int)(n/2))
  # fig, ax = plt.subplots()
  yplot = 2.0/n*np.abs(yf[:n//2])
  cutoff = 0
  for i in range(len(xf)):
    if xf[i] > 4000:
      cutoff = i
      break
  if cutoff > 0:
    # ax.plot(xf[:cutoff], yplot[:cutoff])
    filtered_freq = pd.DataFrame({'magnitude': yplot, 'freq':xf})
  else:
    # ax.plot(xf, yplot)
    filtered_freq = pd.DataFrame({'magnitude': yplot, 'freq':xf})
  
  # print(yf[])
  print(yf[(n//2)-3:(n//2) +3])
  plt.xlabel("Frequency -->")
  plt.ylabel("Magnitude")
  return filtered_freq

file = 'alarm_mono_single.wav'
filtered1 = soundFFT(file)

def initAlarmCSV():
  file = 'alarm_mono_single.wav'
  filtered1 = soundFFT(file)

  freqs = np.arange(0, 4000, 0.1)
  merged_df = pd.DataFrame({'freq': freqs})
  merged_df['freq1'] = pd.Series()
  merged_df['mag1'] = pd.Series()

  #filetered1
  n = 0
  indexFreq = 0
  for freq in freqs:
    tempIndex = n
    while abs((freq - filtered1['freq'][tempIndex])) > abs((freq - filtered1['freq'][tempIndex+1])):
      tempIndex += 1
    
    merged_df['freq1'][indexFreq] = filtered1['freq'][tempIndex]
    merged_df['mag1'][indexFreq] = filtered1['magnitude'][tempIndex]

    n = tempIndex
    n+=1
    indexFreq+=1

  merged_df.to_csv('alarm.csv', index=False)
  
def freqMagMSE(filtered2):
  # Matches up different size and index dataframes in one merged df
  # Takes input two dataframes with columns: 'freq' and 'magnitude
  # Match the closest frequencies up to 4000, then add corresponding magnitudes
  freqs = np.arange(0, 4000, 0.1)
  merged_df = pd.read_csv('alarm.csv')
  merged_df['freq2'] = pd.Series()
  merged_df['mag2'] = pd.Series()

  #filtered2
  n = 0
  indexFreq = 0
  for freq in freqs:
    tempIndex = n
    while abs((freq - filtered2['freq'][tempIndex])) > abs((freq - filtered2['freq'][tempIndex+1])):
      tempIndex += 1
    
    merged_df['freq2'][indexFreq] = filtered2['freq'][tempIndex]
    merged_df['mag2'][indexFreq] = filtered2['magnitude'][tempIndex]

    n = tempIndex
    n+=1
    indexFreq+=1
      
  return mean_squared_error(merged_df['mag1'], merged_df['mag2'])

def checkAlarmSegment(filename):
  filtered = soundFFT(filename)
  mse = freqMagMSE(filtered)
  print(mse)
  if mse > 1.5e-07:
    return False
  else:
    return True

# def makeCoffeeStreamSpeech():
#     while True:
#         chunk = 1024  # Record in chunks of 1024 samples
#         sample_format = pyaudio.paInt16  # 16 bits per sample
#         channels = 1
#         fs = 44100  # Record at 44100 samples per second
#         seconds = 5
#         filename = "d2.wav"
        
#         p = pyaudio.PyAudio()  # Create an interface to PortAudio
#     # 
# #         print('Recording')
#     # 
#         stream = p.open(format=sample_format,
#                         channels=channels,
#                         rate=fs,
#                         frames_per_buffer=chunk,
#                         input=True)

#         frames = []  # Initialize array to store frames

#         # Store data in chunks for 3 seconds
#         for i in range(0, int(fs / chunk * seconds)):
#             data = stream.read(chunk)
#             frames.append(data)

#         # Stop and close the stream 
#         stream.stop_stream()
#         stream.close()
#         # Terminate the PortAudio interface
#         p.terminate()

# #         print('Finished recording')

#         # Save the recorded data as a WAV file
#         wf = wave.open(filename, 'wb')
#         wf.setnchannels(channels)
#         wf.setsampwidth(p.get_sample_size(sample_format))
#         wf.setframerate(fs)
#         wf.writeframes(b''.join(frames))
#         wf.close()
            
            
#         r = sr.Recognizer()
#         audiofile = sr.AudioFile('d2.wav')
#         with audiofile as source:
#             r.adjust_for_ambient_noise(source)
#             audio = r.record(source)
        
#         possible_speech = r.recognize_google(audio, show_all=True)
#         print(possible_speech)
#         if possible_speech != []:
#             for i in possible_speech['alternative']:
#                 print(i)
#                 if 'coffee' in i['transcript']:
#                     print('RUN MOTOR')
#                     RunMotor()
#         print('done')

def makeCoffeeStream():
    while True:
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 1
        fs = 44100  # Record at 44100 samples per second
        seconds = 30
        filename = "d2.wav"
        
        p = pyaudio.PyAudio()  # Create an interface to PortAudio
    # 
#         print('Recording')
    # 
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        # Store data in chunks for 3 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

#         print('Finished recording')

        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
            
            
        # r = sr.Recognizer()
        # audiofile = sr.AudioFile('d2.wav')
        # with audiofile as source:
        #     r.adjust_for_ambient_noise(source)
        #     audio = r.record(source)
        
        possible_alarm = checkAlarmSegment('d2.wav')
        print(possible_alarm)
        if possible_alarm == True:
          print('RUN MOTOR')
        else:
          print('None')
#             RunMotor()
        print('done')

def RunMotor():
    requests.get('http://kartik236.seas.gwu.edu:8080/Start')


if __name__ == "__main__":
#     RunMotor()
    # makeCoffeeStream()
    initAlarmCSV()

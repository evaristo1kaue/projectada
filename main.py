#Usando o Vosk
from importlib.resources import path
from vosk import Model, KaldiRecognizer
import os
import pyttsx3
import json
import core

#Sintese de fala
engine = pyttsx3.init()

if not os.path.exists("model"):
    print("Please download the model from https://alphacephei.com/vosk/model and unpack as 'model' in the current folder.")
    exit(1)

import pyaudio

def speak(text):
    engine.say(text)
    engine.runAndWait()

#Reconhecimento de fala
model = Model ('model')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
stream.start_stream()

#Loop do reconhecimento de fala
text = None
result = None

while True:
    data = stream.read(2048)

    if len(data) == 0:
        break
    
    if rec.AcceptWaveform(data):
        result = rec.Result()
        result = json.loads(result)

    if result is not None:
        text = result['text']

        print(text)

    if text == 'que horas são' or text == 'me diga as horas':
        speak(core.SystemInfo.get_time())
        break

import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from suaBibSignal import signalMeu
import time

print('Começará em 3 segundos')
time.sleep(3)
print('Iniciando gravação')
nome='som.wav'
fs=44100
duration = 5
numAmostras=duration*fs
audio = sd.rec(int(numAmostras), fs, channels=1)
sd.wait()
sf.write(nome, audio, fs)
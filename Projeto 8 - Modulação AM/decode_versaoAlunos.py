#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
from suaBibSignal import signalMeu
from peakutils.plot import plot as pplot
from funcoes_LPF import LPF


def main():

    print("Inicializando decoder")

    # 8. Verifique que o sinal recebido tem a banda dentro de 10kHz e 18kHz (faça o Fourier).
    sinal=signalMeu()
    modulado, fs = sf.read('mod.wav')

    # 9. Demodule o áudio enviado pelo seu colega.
    print('Demodulando o sinal')
    x2,portadora=sinal.generateSin(14000,1,5,fs)
    demodulado=modulado*portadora

    xf, yf = sinal.calcFFT(demodulado, fs)
   
    plt.plot(xf,yf)
    plt.show()
    
    # 10. Filtre as frequências superiores a 4kHz.
    print('Filtrando o sinal')
    freq=4000
    demodulado_lpf=LPF(demodulado,freq,fs)

    xf2, yf2 = sinal.calcFFT(demodulado_lpf, fs)
    
    plt.plot(xf2,yf2)
    plt.show()

    # 11. Execute o áudio do sinal demodulado e verifique que novamente é audível.
    print('Executando o áudio demodulado')
    sd.play(demodulado_lpf, fs)
    sd.wait()

if __name__ == "__main__":
    main()
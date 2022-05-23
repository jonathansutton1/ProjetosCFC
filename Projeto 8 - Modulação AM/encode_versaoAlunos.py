#importe as bibliotecas
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
from suaBibSignal import signalMeu
from funcoes_LPF import LPF

def main():
    sinal=signalMeu()
    print("Inicializando encoder")
    # 1. Faça a leitura de um arquivo de áudio .wav de poucos segundos (entre 2 e 5) previamente gravado com uma
    # taxa de amostragem de 44100Hz.
    data, fs = sf.read('som.wav')

    # 2. Normalize esse sinal: multiplicar o sinal por uma constante (a maior possível), de modo que todos os pontos
    # do sinal permaneçam dentro do intervalo[-1,1].
    time=5
    n = time*fs
    x = np.linspace(0.0, time, n)
    k=1/max(abs(data))
    print(f'Plotando o sinal com k={k}')

    plt.plot(x,k*data)
    plt.show()

    k_data=k*data

    # 3. Filtre e elimine as frequências acima de 4kHz.
    print('Filtrando o sinal')
    freq=4000
    lpf=LPF(k_data,freq,fs)

    print(f'Plotando o sinal com k={k}')
    
    plt.plot(x,lpf)
    plt.show()

    xf, yf = sinal.calcFFT(lpf, fs)
    
    plt.plot(xf,yf)
    plt.show()

    # 4. Reproduza o sinal e verifique que continua audível (com menos qualidade).
    sd.play(lpf, fs)
    sd.wait()

    # Modulando esse sinal de áudio em AM com portadora de 14 kHz. (Essa portadora deve ser uma senoide
    # começando em zero)
    x2,portadora=sinal.generateSin(14000,1,5,fs)

    sinal_modulado=(lpf)*portadora

    plt.plot(x,sinal_modulado)
    plt.show()
    
    xf2, yf2 = sinal.calcFFT(sinal_modulado, fs)
    
    plt.plot(xf2,yf2)
    plt.show()
    

    sf.write('mod.wav', sinal_modulado, fs)
    print('Arquivo de áudio modulado salvo!')

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
import time
import matplotlib as plt
import sounddevice as sd
import numpy as np
from suaBibSignal import *
from scipy.fftpack import fft
from scipy import signal as window
import peakutils 


#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    dic_freq = {1:[1206,697], 2:[1339,697], 3:[1477,697], 4:[1206,770],5:[1339,770], 6:[1477,770], 7:[1206,852], 8:[1339,852], 9:[1477,852]}
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida) 
    bib = signalMeu()
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    freqDeAmostragem = 44100
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = freqDeAmostragem #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    # duration = #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    espera = 2
    print(f'Captação começa em {espera} segundos')
    time.sleep(espera)
   #faca um print informando que a gravacao foi inicializada
    print("Gravação inicializada")
   #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    duracao = 5
   #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    numAmostras = freqDeAmostragem*duracao
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")
    print(audio)
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.linspace(-duracao/2,duracao/2,numAmostras)


    # plot do gravico  áudio vs tempo!
    plt.plot(t,audio[:,0])
    plt.show()
    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signalMeu.calcFFT(signalMeu,audio[:,0], freqDeAmostragem)

    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    plt.show()

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   
    index = peakutils.indexes(yf, thres = 0.3, min_dist = 100)
    print(f'Posicoes X dos picos: {index}')
    print("precisamos encontrar os y")
    picos = list()
    for i in xf[index]:
        picos.append(i)
    
    #printe os picos encontrados! 
    print(f'Picos encontrados: {picos}')
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    listaX = [697,770,852]
    listaY = [1206,1339,1477]
    l,c = 0,0
    for p in picos:
        for t in listaX:
            if t - 10 < p < t+10:
                l = t
        for v in listaY:
            if v - 10 < p < v+10:
                c = v

    #print a tecla.
    num = [c,l]
    print(num)
    for k, x in dic_freq.items():
        if x == num:
            print(f'Tecla digitada: {k} ')
    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()
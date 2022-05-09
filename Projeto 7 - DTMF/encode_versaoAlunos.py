
#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)




def main():
    
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # se voce quiser, pode usar a funcao de construção de senoides existente na biblioteca de apoio cedida. Para isso, você terá que entender como ela funciona e o que são os argumentos.
    # essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # o tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Seja razoável.
    # some as senoides. A soma será o sinal a ser emitido.
    # utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    

    print("Inicializando encoder")
    
    dic_freq = {1:[1206,697], 2:[1339,697], 3:[1477,697], 4:[1206,770],5:[1339,770], 6:[1477,770], 7:[1206,852], 8:[1339,852], 9:[1477,852]}
    NUM = int(input("Digite um Numero entre 1 e 9"))

    print("Aguardando usuário")

    print("Gerando Tons base")
    freq1 = dic_freq[NUM][0]
    freq2 = dic_freq[NUM][1]
    print(freq1)
    print(freq2)

    x, v = signalMeu.generateSin(signalMeu, freq1,1,5,44100)
    x, v2 = signalMeu.generateSin(signalMeu, freq2,1,5,44100)

    sinal = (v+v2)/max(abs(v+v2))
    plt.plot(x,sinal)
    plt.xlim(0,500/44100)
    plt.show()


    print("Executando as senoides (emitindo o som)")
    sinal = (v+v2)/max(abs(v+v2))

    print("Gerando Tom referente ao símbolo : {}".format(NUM))
    sd.play(sinal, 44100)
    # Exibe gráficos

    # aguarda fim do audio
    sd.wait()
    plotFFT(self, signal, fs)
    

if __name__ == "__main__":
    main()

#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


from operator import concat
from enlace import *
import time
import numpy as np
import random

serialName = "COM7"                  # Windows(variacao de)
soma =0
def comando():
    com1 = enlace('COM7')
    dic_comandos = {b'\x00\xff\x00\xff': 4, b'\x00\xff\xff\x00':4, b'\xff':1, b'\x00':1, b'\xff\x00': 2, b'\x00\xff':2 }
    comando1 = b'\x00\xff\x00\xff'
    comando2 = b'\x00\xff\xff\x00'
    comando3 = b'\xff'
    comando4 = b'\x00'
    comando5 = b'\xff\x00'
    comando6 = b'\x00\xff'

    lista_comandos = [comando1,comando2,comando3,comando4,comando5,comando6]
    lista_selecionada = []
    lista_bytes=[]
    i = 0
    numero_comandos = int(input("Escreva um numero entre 10 e 30: "))
    if numero_comandos < 10 or numero_comandos>30 :
        print('NUMERO PASSADO DEVE SER NO MINIMO 10 OU MAXIMO 30\nTENTE NOVAMENTE')
        com1.disable()
    while i < numero_comandos:
        random_add = random.choice(list(dic_comandos.keys()))
        #print(random_add)
        lista_selecionada.append(random_add)
        lista_bytes += ((dic_comandos[random_add]).to_bytes(1, byteorder='big'))
        i += 1
    print(lista_selecionada)
    print(lista_bytes)
    print(len(lista_selecionada))
    

    print(f'tamanho da lista de comandos: {len(lista_selecionada)}')
    print(f'tamanho da lista de bytes: {len(lista_bytes)}')
 
    
    
    t=0
    global soma 
    while t<len(lista_bytes):
        soma += lista_bytes[t]
        t+=1
    soma = soma + numero_comandos
    print (soma)
    return lista_selecionada, lista_bytes

def main():
    try:
        com1 = enlace('COM7')
        
        com1.enable()

        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
  
        print("----------------------------------------------------------")
        print("Comunicação aberta com sucesso! Vamos ao resto do projeto!")
        print("----------------------------------------------------------")

        comandos, tamanhos = comando()
        print("Serao enviadas 2 listas: uma com os bytes, o outro com o comando")

        print("Agora será carregada a imagem em um formato de bytes.")
        
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        print(f"Comandos enviados: {len(comandos)}")       
            
        #finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        if len(comandos) >= 1:
            print("Lista carregada com sucesso! Vamos a transmissão.")
        print(np.asarray(soma.to_bytes(1,byteorder= 'big')))
        com1.sendData(np.asarray(len(comandos).to_bytes(1,byteorder= 'big')))
        time.sleep(0.05)

        conf, nRx =  com1.getData(1)
        print(int.from_bytes(conf, byteorder='big'))

        if int.from_bytes(conf, byteorder='big') != len(comandos):
            print("numero recebido diferente do enviado")
            com1.disable()
        n =0
        while n< len(tamanhos):
            com1.sendData(np.asarray(tamanhos[n].to_bytes(1, byteorder='big')))
            time.sleep(0.05)
            com1.sendData(np.asarray(comandos[n]))
            time.sleep(0.05)             
            print(comandos[n])
            n+=1
        print("enviou")
        
   
        txSize = com1.tx.getStatus()
        print(f"Como o txSize retornou o valor {txSize}, vemos que não deu tempo de transmissão, pois ainda não há nada dentro do buffer..")     

        print("Transmissão completa! O próximo passo é configurar a recepção de dados para o RX.")


        txLen = len(comandos)
        start = time.time()
        rxBuffer, nRx = com1.getData(txLen)
        end = time.time()
        print("recebeu {}" .format(rxBuffer))
        print(f'Tempo de transmissão: {end-start} segundos.')

    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()

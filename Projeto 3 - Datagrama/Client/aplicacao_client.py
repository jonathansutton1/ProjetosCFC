#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#AplicaçãoClient
####################################################


from operator import concat
from enlace import *
import time
import numpy as np
import random

serialName = "COM5"                  # Windows(variacao de)
soma =0
def comando():
    com1 = enlace(serialName)
    dic_comandos = {b'\x00\xff\x00\xff': 4, b'\x00\xff\xff\x00':4, b'\xff':1, b'\x00':1, b'\xff\x00': 2, b'\x00\xff':2 }
 
    lista_selecionada = []
    lista_bytes=[]
    i = 0
    numero_comandos = int(input("Escreva um numero entre 10 e 30: "))
    if numero_comandos < 10 or numero_comandos>30 :
        print('NUMERO PASSADO DEVE SER NO MINIMO 10 OU MAXIMO 30\nTENTE NOVAMENTE')
        com1.disable()
    while i < numero_comandos:
        random_add = random.choice(list(dic_comandos.keys()))
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
        com1 = enlace('COM5')
        
        com1.enable()

        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
  
        print("----------------------------------------------------------")
        print("Transmissão aberta com sucesso! Vamos ao resto do projeto!")
        print("----------------------------------------------------------")

        comandos, tamanhos = comando()
        print("Serao enviadas 2 listas: uma com os bytes, o outro com o comando")
        
        print(f"Quantidade de comandos enviados: {len(comandos)}")       
            
 
        if len(comandos) >= 1:
            print("Lista carregada com sucesso! Vamos a transmissão.")

        print(np.asarray(soma.to_bytes(1,byteorder= 'big')))
        start = time.time()
        com1.sendData(np.asarray(len(comandos).to_bytes(1,byteorder= 'big')))
        time.sleep(0.05)

        conf, nRx =  com1.getData(1)
        print(int.from_bytes(conf, byteorder='big'))

        if int.from_bytes(conf, byteorder='big') != len(comandos):
            print("Tente novamente, o número recebido diferente do enviado")
            com1.disable()
        n =0
        while n< len(tamanhos):
            time.sleep(2)
            com1.sendData(np.asarray(tamanhos[n].to_bytes(1, byteorder='big')))
            time.sleep(0.05)
            com1.sendData(np.asarray(comandos[n]))
            time.sleep(0.05)             
            print(comandos[n])
            n+=1

        end = time.time()
        tempo = end - start
        if tempo >= 10:
            print("Timeout")
            com1.disable()
        else:
            print("Enviado com sucesso")
            print(f"Transmissão completa! Tempo de transmissão: {tempo} segundos.")
    
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

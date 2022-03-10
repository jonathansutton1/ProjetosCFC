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
img = "./pic.jpg"
pri = {'HS': b'\x00', 'msg': b'\x01'}
tipo = {'png':b'\x00','txt': b'\x01', 'jpg': b'\x02'}

def head(str,str1,tamanho,num_pacotes):
    resp1 = pri[str]
    resp2 = tipo[str1]
    #global img
    #pri = {b'\x00': 'HS', b'\x01': 'msg'}
    #tipo = {b'\x00': 'png', b'\x01': 'txt', b'\x02': 'jpg'}
    #tamanho = len(img).to_bytes(3, byteorder='big')
    #num_pacotes = len(img)//114
    lista_head = [resp1,resp2,tamanho,num_pacotes, b'\x00\x00\x00\x00']
    return lista_head

with open(img, "rb") as image: 
    txBuffer = image.read()  #https://stackoverflow.com/questions/22351254/python-script-to-convert-image-into-byte-array


eap = b'\x00\x00\x00\x00'

def pacote(lista_head, payload, eap):
    return [lista_head + payload + eap]


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

        comandos = head('HS','jpg', (len(txBuffer)).to_bytes(3, byteorder='big'), ((len(txBuffer)//114)+1).to_bytes(1, byteorder='big'))
        print(comandos)

        print("Será enviado o primeiro pacote.")        
        print(f"Quantidade de bytes enviados: {len(comandos)}")       
            
 
        if len(comandos) >= 1:
            print("Imagem carregada com sucesso! Vamos a transmissão.")

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

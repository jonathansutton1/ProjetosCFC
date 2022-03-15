#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#AplicaçãoServer
####################################################


from aiohttp import Payload
from enlace import *
import time
import numpy as np

serialName = "COM7"                  # Windows(variacao de)



def main():
    try:

        com1 = enlace(serialName)

        com1.enable()
        print("Esperando 1 byte de sacrifício")        
        rxBuffer, nRx = com1.getData(1)
    
        com1.rx.clearBuffer()
        time.sleep(.1)
        print("----------------------------------------------------------")
        print("Recepcao aberta com sucesso! Vamos ao resto do projeto!")
        print("----------------------------------------------------------")
      
        
        #acesso aos bytes recebidos
        while True:
            pack, nRx = com1.getData(1)
            com1.rx.clearBuffer()
            com1.sendData(pack)
            time.sleep(0.05)
            conf, nRx = com1.getData(1)
            if conf[0] ==2:
                print('confirmacao completa')
                break
        
        x =0
        img=[]
        pack, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        print(pack)
        
        while len(img)<=pack[2]:
            
            pack_H, nRx = com1.getData(1)
            print(pack_H[1], pack_H[3])
            if pack_H.endswith(b'\xFF\xFF\xFF\xFF'):
                com1.rx.clearBuffer()
                img.append(pack_H)
                com1.sendData(np.asarray(pack_H))
                time.sleep(0.05)
            #print(pack_H)
            #print(pack_H[1],pack_H[3])
            #TP = head[1]
            #pack_P, nRx = com1.getData(TP)
            #print(pack_P)
            
        print(len(img))
        
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

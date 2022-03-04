#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#AplicaçãoServer
####################################################


from enlace import *
import time
import numpy as np

serialName = "COM9"                  # Windows(variacao de)


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
        rxBuffer, nRx = com1.getData(1)
        com1.sendData(rxBuffer)
        print(int.from_bytes(rxBuffer, byteorder='big'))
        x=0
        com = []
        start = time.time()
        while x < (int.from_bytes(rxBuffer, byteorder='big')):
            time.sleep(5)
            tam, nRx = com1.getData(1)
            coman, nRx = com1.getData(int.from_bytes(tam, byteorder='big'))
            print(coman)
            com.append(coman) 
            x+=1
        end = time.time()
        time = end - start
        print(com)
        
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

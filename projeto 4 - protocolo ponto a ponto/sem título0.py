#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from threading import Timer
from enlace import *
import time
import numpy as np
import random
# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)



eop= b'\xff\xff\xff\xff'

def calcula_tam(img):
    if len(img)%114==0:
        return len(img)//114
    else:
        return len(img)//114 + 1

def head(tipo, num_pacotes, pacote_at, payload):
    head=[0]*10
    
    tipo_bytes = (tipo).to_bytes(1,byteorder='big')
    num_pacotes_bytes = (num_pacotes).to_bytes(1,byteorder='big')
    pacote_atual_bytes = (pacote_at).to_bytes(1,byteorder='big')
    tam_payload_bytes = (len(payload)).to_bytes(1,byteorder='big')
    id_s = b'\x00'
    
    
    head[0]= tipo_bytes
    head[1]= id_s
    head[2]=b'\x00'
    head[3]=num_pacotes_bytes
    head[4]=pacote_atual_bytes
    if tipo == 1:
        head[5]= b'\x00'
    else:
        head[5]= tam_payload_bytes
    head[6]= b'\x00'
    head[7]= b'\x00'
    head[8]= b'\x00'
    head[9]= b'\x00'


def atualiza (pack, contador):
    contador_bytes = (contador).to_bytes(1,byteorder='big')
    pack[7]= contador_bytes
    return pack

def lista_bytes(bin):
    lista=[]
    



def pacote()    



















































































        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        with open("C:/Users/thpro/Desktop/Camada Física/projetosCamada/p4Protocolo/client/log.txt", "a") as file:
            file.write("Comunicação encerrada")

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

   # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
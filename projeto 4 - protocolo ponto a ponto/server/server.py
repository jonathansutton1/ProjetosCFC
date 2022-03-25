#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)

eop= b'\xff\xff\xff\xff'


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



def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM3')
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        with open("C:/Users/thpro/Desktop/Camada Física/projetosCamada/p4Protocolo/server/log.txt", "w") as file:
            file.write("Comunicação aberta")
            file.write('\n')
        print("Comunicacao aberta")
        
        oci = True
        acabar = False
        
        tempo_S = time.time()
        
        while oci:
            rx, nRX = com1.getData(10)
            time.sleep(0.05)
            eop, nRx = com1.getData(4)
            if rx[0] == 1:
                print("ok")
                if rx[2]== 0:
                    print("ok")
                    oci = False
                    
                    num_pacotes = rx[3]
                    cont = 1
                    ult_succeso=0
                    head2= head(2,num_pacotes, cont, 0)
        
                    pack2=head2+eop
                    print(pack2)
                    
                    com1.sendData(np.asarray(head2))
                    time.sleep(0.05)
            else:
                Tempo_F = time.time()
                if Tempo_F - 20 >= tempo_S:
                    print('time out')
                    oci = True
                    cinco = head(5,0,0,0)
                    cinco = cinco + eop
                    com1.sendData(np.asarray(cinco))
                    
                    acabar=True                    
            if acabar == True:
                print('Acabou')
                break
            time.sleep(1)
        
        if acabar==False:
            packs=[0]*num_pacotes
            while cont <= numPckg:
                confi = False
                timer_S1 = time.time()
            

        




































        com1.disable()
        with open("C:/Users/thpro/Desktop/Camada Física/projetosCamada/p4Protocolo/server/log.txt", "a") as file:
            file.write("Comunicação encerrada")

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
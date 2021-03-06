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
import sys 

from crc import CrcCalculator, Crc16

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM7"                  # Windows(variacao de)


def send(pack, com1):
    com1.sendData(np.asarray(pack))
    time.sleep(.05)
    
dic_tipo = {'um':'env', 'dois':'rec'}
def escreve(num, head):
    type = dic_tipo[num]
    current_time = time.ctime()
    tipo = str(head[0])
    tamanho =str(head[5])
    if type == 'env':
        tipo = str(int.from_bytes(head[0], byteorder='big'))
        tamanho = str(int.from_bytes(head[5], byteorder='big'))
    log = f'{current_time} / {type} / {tipo} / {tamanho}'

    if tipo == '3':
        pacote_enviado = str(head[4])
        num_pacotes = str(head[3])
        if type == 'env':
            pacote_enviado = str(int.from_bytes(head[4], byteorder='big'))
            num_pacotes = str(int.from_bytes(head[3], byteorder='big'))
        log = f"{current_time} / {type} / {tipo} / {tamanho} / {pacote_enviado} / {num_pacotes} / CRC"

    with open('server_Log3.txt', "a") as file:
            file.write(log)
            file.write('\n')
def main():
    try:    

        timer1_start = time.time()

        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        com1.enable()
        
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        

        oci = True 
        payload = [b'\xCC']
        eop = [b'\xff', b'\xff', b'\xff', b'\xff']
        cont = 0

        while oci is True:
            rxBuffer, nRx= com1.getData(10)
            print(rxBuffer[5])
            escreve('dois', rxBuffer)
            num_Pacotes = rxBuffer[3]
            id = rxBuffer[5]
            print(f"id = {id}")

            if id == 20:
                #payload e eop
                rxBuffer, nRx= com1.getData(1)
                rxBuffer, nRx= com1.getData(4)
                oci = False
                time.sleep(1)

            else:
                print("não tem handshake")
                time.sleep(1)

        # tipo 2 
        head = [b'\x02', b'\x00', b'\x00', b'\x01', b'\x01', b'\x14', b'\x00', b'\x01', b'\x00', b'\x00']
        pack = head + payload + eop
        send(pack, com1)
        escreve('um', head)
        cont = 1
        print("handshake enviado")        

        
        while cont <= num_Pacotes:

            timer1_start = time.time()
            timer2_start = time.time()
            acabar = True
            while acabar:

                if com1.rx.getBufferLen() > 0:
                    rxBuffer, nRx= com1.getData(10)
                    escreve('dois', rxBuffer)
                    tipo = rxBuffer[0]
                    pack_recebido = rxBuffer[4]
                    lenPayload = rxBuffer[5]
                    print(f"contador = {cont}")
                    print(f"pack_recibido = {pack_recebido}")
                    if tipo == 3:
                        if pack_recebido == cont:

                            #Tipo 4
                            pay = bytes()
                            for a in payload:
                                pay+=a
                            
                                
                            print(pay)
                            use_table = True
                            crc_calculator = CrcCalculator(Crc16.CCITT, use_table)
                            checksum = crc_calculator.calculate_checksum(pay)                            
                            print(checksum)
                            head = [b'\x04', b'\x00', b'\x00', b'\x01', b'\x01', b'\x01', b'\x00',(cont).to_bytes(1, byteorder='big'), checksum.to_bytes(2, byteorder='big')] 
                            pack = head + payload + eop
                            send(pack, com1)
                            escreve('dois', head)
                            cont += 1
                            print("tipo 4")


                            #payload e eop
                            rxBuffer, nRx= com1.getData(lenPayload)
                            rxBuffer, nRx= com1.getData(4)

                            acabar = False

                        else:

                            # tipo 6
                            head = [b'\x06', b'\x00', b'\x00', b'\x01', b'\x01', b'\x01', (cont).to_bytes(1, byteorder='big'),(cont-1).to_bytes(1, byteorder='big'), b'\x00', b'\x00'] 
                            pack = head + payload + eop
                            send(pack,com1)
                            escreve('um', head)
                            print("tipo 6")

                            #payload e eop
                            rxBuffer, nRx= com1.getData(lenPayload)
                            rxBuffer, nRx= com1.getData(4)
                            acabar = False

                else:
                    time.sleep(1)
                    timer2 = time.time() - timer2_start
                    timer1 = time.time() - timer1_start

                    if timer2 > 200:
                        oci = True
                        # tipo 5
                        head = [b'\x05', b'\x00', b'\x00', b'\x01', b'\x01', b'\x01', b'\x00',(cont).to_bytes(1, byteorder='big'), b'\x00', b'\x00'] 
                        pack = head + payload + eop
                        send(pack, com1) 
                        escreve('um', head)
                        print("tipo 5 (time out)")
                        # Encerra comunicação
                        print("-------------------------")
                        print("Comunicação encerrada")
                        print("-------------------------")
                        com1.disable()
                        sys.exit()
                    
                    if timer1 > 2:

                        # tipo 4
                        
                        
                        head = [b'\x04', b'\x00', b'\x00', b'\x01', b'\x01', b'\x01', b'\x00',(cont).to_bytes(1, byteorder='big'), b'\x00', b'\x00'] 
                        pack = head + payload + eop
                        send(pack, com1)
                        escreve('um', head)
                        print("tipo 4 reenviada")
                        timer1_start = time.time()

        print("Sucesso :)")
        com1.disable()       
                    
            
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

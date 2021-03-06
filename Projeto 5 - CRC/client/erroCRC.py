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
from random import randrange

from crc import CrcCalculator, Crc16

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM8"                  # Windows(variacao de)


def cria_payloads(sorteio):

    comandos = []
    num = 0
    while num < sorteio:
        comandos += [b"\xab", b"\xab", b"\xab", b"\xab", b"\xab", b"\xab", b"\xab", b"\xab"]
        num += 1
        
    numPack = len(comandos) // 114
    ultimo = len(comandos) % 114
    
    if ultimo > 0:
        numPack += 1
    
    lista_payloads = []
    a = 0
    z = 114
    print(f"{numPack} pacotes")
    for n in range(numPack):                
        if ultimo > 0:
            if n < numPack - 1:
                lista_payloads.append(comandos[a:z])
                a += 114
                z += 114
            elif n == numPack-1:
                z -= 114
                z +=  ultimo     
                lista_payloads.append(comandos[a:z])
            
            else:
                lista_payloads.append(comandos[a:z])
                a += 114
    return lista_payloads, numPack
  

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

    with open('client_Log3.txt', 'a') as file:
            file.write(log)
            file.write('\n')

def main():
    try:

        # sorteio número de pacotes a serem enviados
        sorteio = randrange(70, 150)
        print(f"sorteio = {sorteio}")

        lista_payloads, numPack = cria_payloads(sorteio)


        com1 = enlace(serialName)
        com1.enable()

          
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
          
        
        inicia = False 
        cont = 0
        eop = [b'\xff', b'\xff', b'\xff', b'\xff']
        
        # handshake
        while inicia is False:

            payload = [b'\xCC']
            head = [b'\x01', b'\x00', b'\x00', (numPack).to_bytes(1,byteorder="big"), b'\x01', b'\x14', b'\x00', b'\x00', b'\x00', b'\x00']
            pack = head + payload + eop
            send(pack, com1)
            print(head)
            escreve('um', head)
            print("handshake enviado")

            time.sleep(5)

            rxBuffer, nRx = com1.getData(10)
            print(rxBuffer[5])
            escreve('dois',rxBuffer)



            tipo = rxBuffer[0]

            # recebiemnto confirm
            if tipo == 2:

                id = rxBuffer[5]
                pac_confirmation = rxBuffer[7]

                if id == 20 and pac_confirmation == 1:
                    inicia = True
                    cont = 1
            
            #payload e eop
            rxBuffer, nRx = com1.getData(1)
            rxBuffer, nRx = com1.getData(4)
            print(f"numPack = {numPack}")

        while cont <= numPack:
            #TIPO 3
            payload = lista_payloads[cont-1]
            
            pay = bytes()
            for a in payload:
                pay += a
            print(pay)
            use_table = True
            crc_calculator = CrcCalculator(Crc16.CCITT, use_table)
            checksum = crc_calculator.calculate_checksum(pay)
            if checksum != pay:
                print("Deu erro")

            print(f'CRC:checksum')
            
            head = [b'\x03', b'\x00', b'\x00', (numPack).to_bytes(1,byteorder="big"), (cont).to_bytes(1,byteorder="big"), (len(payload)).to_bytes(1,byteorder="big"), b'\x00',b'\x00', checksum.to_bytes(2, byteorder='big')]
            pack = head + payload + eop
            print(pack)
            print('CHECK BYTES', head[8])

            send(pack, com1)
            escreve('um', head)
            print("tipo 3 enviado")

            timer1_start = time.time()
            timer2_start = time.time()

            acabar = True

            while acabar:
                timer1 = time.time() - timer1_start
                timer2 = time.time() - timer2_start

                if timer1 > 5.0:
                    send(pack, com1)
                    escreve('um', head)
                    print("tipo 3 reenviada")
                    timer1_start = time.time()
                
                elif timer2 > 20.0:

                    #TIPO 5
                    payload = [b'\x0F']
                    head = [b'\x05', b'\x00', b'\x00', (numPack).to_bytes(1,byteorder="big"), b'\x01', b'\x00', b'\x00',b'\x00', b'\x00', b'\x00'] 
                    pack = head + payload + eop
                    send(pack, com1)
                    escreve('um', head)
                    print("tipo 5 enviado")
                    print("Time out")

                    #Encerra comunicação
                    print("-------------------------")
                    print("Comunicação encerrada")
                    print("-------------------------")
                    com1.disable()
                    sys.exit()

                
                elif com1.rx.getBufferLen() > 0:

                    rxBuffer, nRx = com1.getData(10)
                    escreve('dois', rxBuffer)
                    tipo = rxBuffer[0]

                    #Tipo 6
                    if tipo == 6:
                        print("Tipo 6 recebido")
                        lastPack = rxBuffer[6]
                        cont = lastPack

                        #Reenvia Tipo 3
                        payload = lista_payloads[cont-1]
                        head = [b'\x03', b'\x00', b'\x00', (numPack).to_bytes(1,byteorder="big"), (cont).to_bytes(1,byteorder="big"), (len(payload)).to_bytes(1,byteorder="big"), b'\x00',b'\x00', b'\x00', b'\x00']
                        pack = head + payload + eop
                        send(pack, com1)
                        escreve('um', head)
                        print("mensagem 3 reenviada")

                        #payload e eop
                        rxBuffer, nRx = com1.getData(1)
                        rxBuffer, nRx = com1.getData(4)

                        timer1_start = time.time()
                        timer2_start = time.time()
                    
                    #Tipo 4
                    elif tipo == 4:
                        print("tipo 4 recebida")
                        cont += 1

                        rxBuffer, nRx = com1.getData(1)
                        rxBuffer, nRx = com1.getData(4)

                        acabar = False


        print("sucesso :)")

    
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

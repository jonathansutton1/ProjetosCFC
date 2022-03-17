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

serialName = "COM8"                  # Windows(variacao de)
soma =0
img = "./pic.jpg"
pri = {'HS': (b'\x00'), 'msg': b'\x01', 'certo':b'\x02'}

def head(str,payload,num_pacotes, pacote):
    resp1 = pri[str]
    return resp1+payload+num_pacotes+pacote+ b'\x00\x00\x00\x00\x00\x00'
    

with open(img, "rb") as image: 
    txBuffer = image.read()  #https://stackoverflow.com/questions/22351254/python-script-to-convert-image-into-byte-array


eop = b'\xFF\xFF\xFF\xFF'

    
    



def main():
    try:
        com1 = enlace('COM8')
        
        com1.enable()

        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
        print("----------------------------------------------------------")
        print("Transmissão aberta com sucesso! Vamos ao resto do projeto!")
        print("----------------------------------------------------------")
        
        
        
        modo = 'HS'
        payload = b'\x01'
        n_pac=(((len(txBuffer)//114)+1))
        head_HS = head(modo, payload, (n_pac).to_bytes(1, byteorder='big') , b'\x00')
        print(head_HS[2])
        print(head_HS)
        HS = head_HS + payload + eop
        print(HS)
        print(np.asarray(HS))
        print("HS enviado")
        
        
        

        while True:
            com1.sendData(np.asarray(HS))
            time.sleep(0.05)
            conf, nRX = com1.getData(1)
            if conf != HS:
                print('ERRO')
                r = input('Quer tentar novamnete? [y/n]')
                if r != 'y':
                    com1.disable()
                    break
            else:
                head_HS = head('certo', payload, (n_pac).to_bytes(1, byteorder='big') , b'\x00')
                HS = head_HS + payload + eop
                com1.sendData(np.asarray(HS))
                time.sleep(0.05)
                print('certo')
                break
               
            
            
        print('Comecando a Enviar a IMG')
        modo = 'msg'
        print(len(payload))
        
        com1.rx.clearBuffer()
        
        head_HS = head(modo, payload, (n_pac).to_bytes(1, byteorder='big') , b'\x00')
        HS = head_HS + payload + eop
        print(HS)
        com1.sendData(np.asarray(HS))
        time.sleep(0.05)
        print('oi')
        
        
        
        
        pacote = 1
        while pacote <= (len(txBuffer)//114)+1:
            
            while True:
                confi, nRX = com1.getData(1)
                if confi.endswith(b'\xFF\xFF\xFF\xFF'):
                    com1.rx.clearBuffer()
                    break
                
            if confi[0] == 1:
                tp=(len(payload)).to_bytes(1, byteorder='big')
                h = head(modo, tp, (n_pac).to_bytes(1, byteorder='big') , (pacote).to_bytes(1, byteorder='big'))
                print(h[2])
                payload = txBuffer[((pacote-1)*114):(114*(pacote))]
                if h[3] == h[2]:
                    payload = txBuffer[((pacote-1)*114):]
                    tp=(len(payload)).to_bytes(1, byteorder='big')
                    h = head(modo, tp, (n_pac).to_bytes(1, byteorder='big') , (pacote).to_bytes(1, byteorder='big'))
                print(len(payload))
                MSG = h + payload + eop
                print(MSG[1],MSG[3])
                com1.sendData(np.asarray(MSG))
                time.sleep(0.05)
                pacote+=1
            
        print('Enviou tudo')  
             

        
        #print("Será enviado o primeiro pacote.")        
        #print(f"Quantidade de bytes enviados: {len(comandos)}")       
            
 
        #if len(comandos) >= 1:
        print("Imagem carregada com sucesso! Vamos a transmissão.")

        print(np.asarray(soma.to_bytes(1,byteorder= 'big')))
        start = time.time()
        com1.sendData(np.asarray(pacote()))
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

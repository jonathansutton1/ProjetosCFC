#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


from enlace import *
import time
import numpy as np
import random

serialName = "COM5"                  # Windows(variacao de)

def comandos():
    com1 = enlace('COM5')
    dic_comandos = {b'\x00\xff\x00\xff': 4, b'\x00\xff\xff\x00':4, b'\xff':1, b'\x00':1, b'\xff\x00': 2, b'\x00\xff':2 }
    comando1 = b'\x00\xff\x00\xff'
    comando2 = b'\x00\xff\xff\x00'
    comando3 = b'\xff'
    comando4 = b'\x00'
    comando5 = b'\xff\x00'
    comando6 = b'\x00\xff'

    lista_comandos = [comando1,comando2,comando3,comando4,comando5,comando6]
    dic_seleciondos = {}
    lista_selecionada = []
    lista_bytes=[]
    i = 0
    numero_comandos = int(input("Escreva um numero entre 10 e 30: "))
    if numero_comandos < 10:
        print('NUMERO PASSADO DEVE SER NO MINIMO 10')
        com1.disable()
    while i < numero_comandos:
        random_add = random.choice(list(dic_comandos.keys()))
        dic_seleciondos.append(random_add)
        lista_selecionada.append(random_add)
        lista_bytes.append(bin(dic_comandos[random_add]))
        dic_seleciondos[random_add] = bin(dic_comandos[random_add])
        i += dic_comandos[random_add]
        
    print(f'tamanho da lista de comandos: {len(lista_selecionada)}')
    print(f'tamanho da lista de bytes: {len(lista_bytes)}')
    print (dic_seleciondos)
    
    return lista_selecionada,lista_bytes

def main():
    try:
        com1 = enlace('COM5')
        
        com1.enable()
  
        print("----------------------------------------------------------")
        print("Comunicação aberta com sucesso! Vamos ao resto do projeto!")
        print("----------------------------------------------------------")

        txBuffer = comandos()
        print("Serao enviadas 2 listas: uma com os bytes, o outro com o comando")

        print("Agora será carregada a imagem em um formato de bytes.")
        
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        print(f"Bytes enviados: {len(txBuffer)}")       
            
        #finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        if len(txBuffer) >= 1:
            print("Imagem carregada com sucesso! Vamos a transmissão.")
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!
          
          
  
        #txBuffer = #dados
        com1.sendData(np.asarray(txBuffer))
        #time.sleep(1.5)
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        txSize = com1.tx.getStatus()
        print(f"Como o txSize retornou o valor {txSize}, vemos que não deu tempo de transmissão, pois ainda não há nada dentro do buffer..")     
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        print("Transmissão completa! O próximo passo é configurar a recepção de dados para o RX.")
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        txLen = len(txBuffer)
        start = time.time()
        rxBuffer, nRx = com1.getData(txLen)
        end = time.time()
        print("recebeu {}" .format(rxBuffer))
        print(f'Tempo de transmissão: {end-start} segundos.')

            
        print("Salvando dados no arquivo novo")
        print("- {}".format(imageW))
        f = open(imageW,'wb')
        f.write(rxBuffer)
        f.close()

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

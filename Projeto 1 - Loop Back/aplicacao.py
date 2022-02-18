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
serialName = "COM7"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM7')
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("----------------------------------------------------------")
        print("Comunicação aberta com sucesso! Vamos ao resto do projeto!")
        print("----------------------------------------------------------")

        imageR = "./img/wpp.png"
        imageW = "./img/CopiaDevolvida.png"
        
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esta sempre irá armazenar os dados a serem enviados.
        print("Agora será carregada a imagem em um formato de bytes.")
        with open(imageR, "rb") as image: 
            print(" - {}".format(imageR))
            txBuffer = image.read()  #https://stackoverflow.com/questions/22351254/python-script-to-convert-image-into-byte-array

            #tinha criado uma lista pra append os bytes, mas deu erro
        #print(txBuffer)

        
        #txBuffer = imagem em bytes!
    

    
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

#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
import random

command1 = b'\x00\x00\x00\x00'
command2 = b'\x00\x00\xBB\x00'
command3 = b'\xBB\x00\x00'
command4 = b'\x00\xBB\x00'
command5 = b'\x00\x00\xBB'
command6 = b'\x00\xAA'
command7 = b'\xBB\x00'
command8 = b'\x00'
command9 = b'\xBB'

commands = [command1,command2,command3,command4,command5,command6,command7,command8,command9]

quantidade = random.randint(10,30)

def sorteia_comandos():
    random_commands = []
    i = 1
    while i <= quantidade:
        sorteado = random.randint(0,8)
        random_commands.append(commands[sorteado])
        i+=1
    return random_commands

def constroi_mensagem(lista_comandos):
    total = len(lista_comandos)
    mensagem = bytearray([total])
    for command in lista_comandos:
        mensagem += command
        mensagem += b'\xFB'
    return mensagem    
    
    

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
        
        print("Iniciou o main")
        
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        com1.enable()
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")


        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        print("Sorteando comandos e construíndo mensagens")
        comandos = sorteia_comandos()
        print(f"Serão enviados {len(comandos)} comandos")
        print(comandos)
        txBuffer = constroi_mensagem(comandos)
        print(txBuffer)
        #txBuffer = b'\x12\x13\xAA'  #isso é um array de bytes
       
        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
               
        
        com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
          
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        while com1.tx.getIsBussy():
            pass
        
        txSize = com1.tx.getStatus()
        print('enviou = {}' .format(txSize))
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        #txLen = len(txBuffer)
        #rxBuffer, nRx = com1.getData(10)
        #print("recebeu {} bytes" .format(len(rxBuffer)))
        
        #for i in range(len(rxBuffer)):
            #print("recebeu {}" .format(rxBuffer[i]))
        
        #print(rxBuffer)
        #fecha arquivo de imagem

            
    
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

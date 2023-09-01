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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)

def split_message(message):
    message = bytearray(message)
    message.pop(0)
    m = message.split(b'\xfb')
    while b'' in m:
        m.remove(b'')
    return m

# def get_first(message):
#     return message[0]

def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        print("esperando 1 byte de sacrifício")

        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)


        mensagem = b''

        #acesso aos bytes recebidos
        while True:
            rxBuffer, nRx = com1.getData(1)
            print("tenho {} bytes" .format(com1.rx.getBufferLen()))
            mensagem += rxBuffer
            print(mensagem)

            if com1.rx.getBufferLen() == 0:
                mensagens = split_message(mensagem)
                break
        
        print('a'*50)
        mensagens = mensagens
        print(mensagens)
        
        num_comandos = len(mensagens)

        total_bytes = 0
        for mensagem in mensagens:
            print(f"Recebi a mensagem {mensagem}")
            total_bytes += len(mensagem)

        print(f"Recebi {num_comandos} comandos, totalizando {total_bytes} bytes!")
        
        #for i in range(len(rxBuffer)):
            #print("recebeu {}" .format(rxBuffer[i]))
        
        confirmacao = bytearray([num_comandos])
        #confirmacao = bytearray([9])
        com1.sendData(confirmacao)

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

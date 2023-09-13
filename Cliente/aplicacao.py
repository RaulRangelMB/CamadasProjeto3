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
import datetime

EOP = b"/xfb/xfb/xfb"

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

quantidade = random.randint(50,70)

def sorteia_comandos():
    random_commands = []
    i = 1
    while i <= quantidade:
        sorteado = random.randint(0,8)
        random_commands.append(commands[sorteado])
        i+=1
    return random_commands

def constroi_mensagem(informacao):
    mensagem = bytearray([])
    for command in informacao:
        mensagem += command
        mensagem += b'\xFB'
    return mensagem    

def constroi_head(posicao, total_pacotes, tamanho_payload, handshake):
    if not (0 <= posicao <= 255 and 0 <= total_pacotes <= 255 and 0 <= tamanho_payload <= 255 and 0 <= handshake <= 255):
        raise ValueError("Os valores devem estar no intervalo de 0 a 255.")
    byte_array = bytearray([0] * 12)
    
    byte_array[0:1] = int.to_bytes(posicao,1,byteorder='little')
    byte_array[1:2] = int.to_bytes(total_pacotes,1, byteorder='little')
    byte_array[2:3] = int.to_bytes(tamanho_payload,1, byteorder='little')
    byte_array[-1:0] = int.to_bytes(handshake,1, byteorder='little')

    return byte_array

def constroi_datagramas(lista_payloads):
    datagramas = []
    posicao = 0
    total_pacotes = len(lista_payloads)
    for payload in lista_payloads:
        print(payload)
        tamanho_payload = len(payload)
        head = constroi_head(posicao, total_pacotes, tamanho_payload, 0)
        print("b")
        print(head)
        datagrama = head + payload
        print(datagrama)
        print("a")
        datagrama = datagrama + EOP
        
        datagramas.append(datagrama)
    return datagramas
        
    
def constroi_pacotes(mensagem):
    print(type(mensagem))
    pacotes = []
    i = 0
    while i < len(mensagem):
        pacote = bytearray([])
        while len(pacote) < 50 and i < len(mensagem):
            pacote.append(mensagem[i])
            i += 1
        pacotes.append(pacote)
        print(len(pacote))
    return pacotes
    

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
        lista = constroi_pacotes(txBuffer)
        #print(lista)
        datagramas = constroi_datagramas(lista)
        print(datagramas)
        
        
        
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
        
        mensagem = b''
        tempo_inicio = datetime.datetime.now()
        recebeu = False
        while (datetime.datetime.now() - tempo_inicio < datetime.timedelta(seconds=5)) and not recebeu:
            if com1.rx.getBufferLen() > 0:
                recebeu = True
                rxBuffer, nRx = com1.getData(1)
                mensagem += rxBuffer
            
            #print(mensagem)
            
        if not recebeu:
            print("TIME OUT")
        else:
            comandos_recebidos = int.from_bytes(mensagem, byteorder='little')

            print(f"O servidor informou que recebeu {comandos_recebidos} comandos")
            if comandos_recebidos != len(comandos):
                print(f"INCONSISTÊNCIA: Foram enviados {len(comandos)} e recebidos {comandos_recebidos}")
            if comandos_recebidos == len(comandos):
                print("SUCESSO")
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

import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

nome = input("Nome do utilizador: ")
client.send(nome.encode())

print("Conectado ao chat! Escreve 'sair' para sair.\n")

def receber_mensagens():
    while True:
        try:
            mensagem = client.recv(1024).decode()
            print("\n" + mensagem)
        except:
            break

# Thread para receber mensagens
thread_receber = threading.Thread(target=receber_mensagens)
thread_receber.daemon = True
thread_receber.start()

while True:
    mensagem = input()
    client.send(mensagem.encode())

    if mensagem.lower() == "sair":
        break

client.close()

import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

clientes = []  # lista de (conn, nome)

def broadcast(mensagem, conn_origem):
    for cliente, _ in clientes:
        if cliente != conn_origem:
            try:
                cliente.send(mensagem.encode())
            except:
                cliente.close()

def lidar_com_cliente(conn, addr):
    try:
        # Receber nome do cliente
        nome = conn.recv(1024).decode()
        clientes.append((conn, nome))

        print(f"{nome} entrou no chat.")
        broadcast(f"🔔 {nome} entrou no chat.", conn)

        while True:
            mensagem = conn.recv(1024).decode()

            if not mensagem or mensagem.lower() == "sair":
                break

            msg_formatada = f"{nome}: {mensagem}"
            print(msg_formatada)
            broadcast(msg_formatada, conn)

    except:
        pass

    # Cliente saiu
    print(f"{nome} saiu do chat.")
    broadcast(f"❌ {nome} saiu do chat.", conn)

    clientes.remove((conn, nome))
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Servidor de chat ativo...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(
        target=lidar_com_cliente,
        args=(conn, addr)
    )
    thread.start()

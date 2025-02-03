import socket
import threading


# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 12345        # Porta do servidor

# Lista para armazenar os clientes conectados
clients = []
names = {}

def broadcast(message, sender_socket):
    """Função para retransmitir mensagens para todos os clientes."""
    for client in clients:
        if client != sender_socket:  # Evita enviar a mensagem de volta para o remetente
            try:
                client.send(message.encode('utf-8'))
            except:
                # Remove clientes desconectados
                clients.remove(client)

def handle_client(client_socket):
    """Função para lidar com mensagens de um cliente."""
    try:
        # Recebe o nome do cliente
        name = client_socket.recv(1024).decode('utf-8')
        names[client_socket] = name
        print(f"{name} se conectou.")

        # Informa os outros clientes
        broadcast(f"{name} entrou no chat.", client_socket)

        while True:
            # Recebe mensagem do cliente
            message = client_socket.recv(1024).decode('utf-8')
            if message.lower() == 'sair':
                print(f"{name} saiu do chat.")
                broadcast(f"{name} saiu do chat.", client_socket)
                break

            # Adiciona o nome do remetente e retransmite a mensagem
            formatted_message = f"{name}: {message}"
            broadcast(formatted_message, client_socket)

    except Exception as e:
        print(f"Erro com o cliente {names.get(client_socket, 'desconhecido')}: {e}")

    finally:
        # Remove o cliente desconectado
        clients.remove(client_socket)
        client_socket.close()
        del names[client_socket]

# Configurando o servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Servidor iniciado em {HOST}:{PORT}")

# Aceitando conexões de clientes
try:
    while True:
        client_socket, client_address = server.accept()
        print(f"Conexão de {client_address}")

        # Adiciona o cliente na lista de conexões
        clients.append(client_socket)

        # Cria uma thread para lidar com o cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

except KeyboardInterrupt:
    print("Encerrando o servidor...")
    server.close()
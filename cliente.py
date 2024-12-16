"--- CLIENTE ---"

import socket
import threading

def receive_messages(client_socket):
    """Função para receber mensagens do servidor."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Conexão com o servidor foi encerrada.")
            break

def client_program():
    """Cliente do chat."""
    HOST = '127.0.0.1'
    PORT = 12345

    # Configura o socket do cliente
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Envia o nome do cliente
    name = input("Digite seu nome: ")
    client.send(name.encode('utf-8'))

    # Cria uma thread para receber mensagens do servidor
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    # Envia mensagens ao servidor
    try:
        while True:
            message = input()
            if message.lower() == 'sair':
                client.send('sair'.encode('utf-8'))
                break
            client.send(message.encode('utf-8'))

    except KeyboardInterrupt:
        pass

    finally:
        print("Encerrando cliente...")
        client.close()

if __name__ == "__main__":
    client_program()

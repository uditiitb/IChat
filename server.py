import threading
import socket

HOST = 'localhost'
PORT = 10000

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message.encode())
    

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode()
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!')
            nicknames.remove(nickname)
            client.close()
            break

def recieve():
    while True:
        client,address = server.accept()
        clients.append(client)

        while True:
            if(client.recv(1024).decode()=='NICK'):
                nickname = client.recv(1024).decode()
                nicknames.append(nickname)
                print(f'Connected with {nickname}')
                broadcast(f'{nickname} joined!')
                client.send('Connected to server'.encode())
                break

        thread = threading.Thread(target = handle,args= ((client,)))
        thread.start()

print('server is listening!')
recieve()



